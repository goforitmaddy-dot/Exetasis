from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from backend.app.core.config import settings

Base = declarative_base()

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
)

async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency that provides an async database session."""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def migrate_agent_evaluation_nullable_score(conn) -> None:
    """Add nullable score/status columns without rebuilding or dropping the legacy table."""
    evaluation_info = await conn.exec_driver_sql("PRAGMA table_info(agent_evaluations)")
    evaluation_columns = evaluation_info.fetchall()
    if not evaluation_columns:
        return
    columns_by_name = {row[1]: row for row in evaluation_columns}
    has_status = "evaluation_status" in columns_by_name
    if "score_nullable" not in columns_by_name:
        # Adding a nullable column preserves the legacy NOT NULL score, all existing indexes,
        # table constraints, triggers, and foreign-key relationships without a destructive rebuild.
        await conn.exec_driver_sql("ALTER TABLE agent_evaluations ADD COLUMN score_nullable FLOAT NULL")
        await conn.exec_driver_sql(
            "UPDATE agent_evaluations SET score_nullable = score "
            "WHERE score_nullable IS NULL AND score IS NOT NULL"
        )
    if not has_status:
        await conn.exec_driver_sql(
            "ALTER TABLE agent_evaluations ADD COLUMN evaluation_status VARCHAR(30) NOT NULL DEFAULT 'evaluated'"
        )
    await conn.exec_driver_sql("CREATE INDEX IF NOT EXISTS ix_agent_evaluations_evaluation_status ON agent_evaluations (evaluation_status)")


async def init_db() -> None:
    """Initialize database tables on application startup."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # Small additive migration for existing MVP SQLite databases (create_all does not alter tables).
        if "sqlite" in settings.DATABASE_URL:
            for table, additions in {
                "workplace_events": {
                    "organization_id": "VARCHAR(36)",
                    "source_identifier": "VARCHAR(255)",
                },
                "employees": {"organization_id": "VARCHAR(36)"},
            }.items():
                columns = await conn.exec_driver_sql(f"PRAGMA table_info({table})")
                present = {row[1] for row in columns.fetchall()}
                for column, sql_type in additions.items():
                    if column not in present:
                        await conn.exec_driver_sql(f"ALTER TABLE {table} ADD COLUMN {column} {sql_type}")
            await conn.exec_driver_sql(
                "CREATE UNIQUE INDEX IF NOT EXISTS uq_event_source_identifier "
                "ON workplace_events (source, source_identifier)"
            )
            await migrate_agent_evaluation_nullable_score(conn)
