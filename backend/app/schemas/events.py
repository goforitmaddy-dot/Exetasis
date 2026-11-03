from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class WorkplaceEventBase(BaseModel):
    """Base schema for workplace events."""

    source: str = Field(..., description="Source adapter (slack, github, calendar, manual)")
    organization_id: str | None = None
    source_identifier: str | None = None
    event_type: str = Field(..., description="Type of event, e.g. commit, pr_review, chat_message")
    employee_id: Optional[str] = Field(None, description="Employee identifier, if associated")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary event payload data")


class WorkplaceEventCreate(WorkplaceEventBase):
    """Event ingestion schema."""

    pass


class WorkplaceEventRead(WorkplaceEventBase):
    """Event schema as stored and returned by API."""

    id: str
    processed: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EventBatchIngestRequest(BaseModel):
    """Schema for ingesting a batch of events."""

    events: List[WorkplaceEventCreate] = Field(..., min_length=1)


class EventIngestResponse(BaseModel):
    """Response confirming event ingestion."""

    ingested_count: int
    event_ids: List[str]
    status: str = "success"
