import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import ValidationError

from backend.app.core.logging import logger
from backend.app.db.models.event import WorkplaceEvent
from backend.app.db.models.orchestration import OrchestrationRun
from backend.app.db.repositories.event_repo import EventRepository
from backend.app.db.repositories.metric_repo import MetricRepository
from backend.app.schemas.events import WorkplaceEventCreate
from backend.app.schemas.orchestration import ContributionResult, OrchestrationRunRead
from backend.app.services.event_service import EventService
from backend.app.services.llm.factory import get_llm_client
from backend.app.orchestration.event_graph import build_event_graph
from backend.app.websocket.connection_manager import manager
from backend.app.schemas.digital_twin import TwinServerUpdateMessage


class OrchestrationService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def run_event(self, event_id: str | None = None, event: dict[str, Any] | None = None) -> OrchestrationRunRead:
        if event is not None:
            db_event_read = await EventService(self.session).ingest_single(WorkplaceEventCreate.model_validate(event))
            event_id = db_event_read.id
        if not event_id:
            raise ValueError("Provide event_id or event data.")

        db_event = await EventRepository(self.session).get_by_id(event_id)
        if not db_event:
            raise LookupError(f"Event '{event_id}' was not found.")
        existing_q = await self.session.execute(
            select(OrchestrationRun).where(OrchestrationRun.event_id == event_id).order_by(OrchestrationRun.created_at.desc()).limit(1)
        )
        run = existing_q.scalars().first()
        if run and run.status in {"completed", "skipped"}:
            return self._read(run)
        if run is None:
            run = OrchestrationRun(id=str(uuid.uuid4()), event_id=db_event.id, organization_id=db_event.organization_id, status="running", result={})
            self.session.add(run)
            await self.session.flush()
        else:
            run.status = "running"
            run.error = None
        # Keep the ingested event and execution trace durable before agent work starts.
        await self.session.commit()

        logger.info("Orchestration run %s started for event %s", run.id, db_event.id)
        try:
            graph = build_event_graph(self.session, db_event, get_llm_client())
            state = await graph.ainvoke({"event": {
                "id": db_event.id,
                "organization_id": db_event.organization_id,
                "source_identifier": db_event.source_identifier,
                "source": db_event.source,
                "event_type": db_event.event_type,
                "employee_id": db_event.employee_id,
                "payload": db_event.payload,
                "created_at": db_event.created_at.isoformat() if db_event.created_at else None,
            }})
            if state.get("error"):
                run.status = "failed"
                run.error = str(state["error"])[:500]
                run.result = {}
                await self.session.commit()
                return self._read(run)
            run.status = state.get("status", "completed")
            run.result = {k: state[k] for k in ("contribution", "update") if k in state}
            await self.session.commit()
            # Publish only after the event, metric result, and run record are durable.
            if "update" in state:
                update = state["update"]
                try:
                    message = TwinServerUpdateMessage(
                        event_type="metric_alert",
                        node_id=update.get("employee_or_department_id"),
                        delta=update,
                        timestamp=update.get("timestamp"),
                    )
                    await manager.broadcast(message.model_dump(mode="json"))
                except Exception as exc:
                    logger.warning("Digital Twin update failed after committed run %s: %s", run.id, exc)
            logger.info("Orchestration run %s finished with status %s", run.id, run.status)
        except Exception as exc:
            logger.exception("Orchestration run %s failed for event %s", run.id, db_event.id)
            await self.session.rollback()
            run = await self.session.get(OrchestrationRun, run.id)
            if run is None:
                raise
            run.status = "failed"
            run.error = str(exc)[:500]
            await self.session.commit()
        return self._read(run)

    async def get_run(self, run_id: str) -> OrchestrationRunRead | None:
        result = await self.session.execute(select(OrchestrationRun).where(OrchestrationRun.id == run_id))
        run = result.scalars().first()
        if not run:
            return None
        read = self._read(run)
        saved_result = await MetricRepository(self.session).get_by_event_and_agent(run.event_id, "contribution")
        if saved_result:
            persisted = saved_result.metadata_json
            try:
                persisted = ContributionResult.model_validate(persisted).model_dump(mode="json")
            except ValidationError:
                # Preserve legacy metadata from records written before the structured contract existed.
                logger.warning("Legacy contribution result %s does not match the current result schema", saved_result.id)
            read.result = {**read.result, "contribution": persisted}
        return read

    async def list_runs(self, organization_id: str, limit: int = 50) -> list[OrchestrationRunRead]:
        result = await self.session.execute(
            select(OrchestrationRun).where(OrchestrationRun.organization_id == organization_id)
            .order_by(OrchestrationRun.created_at.desc()).limit(limit)
        )
        return [self._read(run) for run in result.scalars().all()]

    @staticmethod
    def _read(run: OrchestrationRun) -> OrchestrationRunRead:
        return OrchestrationRunRead(
            run_id=run.id,
            event_id=run.event_id,
            organisation_id=run.organization_id,
            status=run.status,
            result=run.result or {},
            error=run.error,
            created_at=run.created_at,
            updated_at=run.updated_at,
        )
