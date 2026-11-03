from sqlalchemy import Column, JSON, String

from backend.app.db.session import Base


class Organization(Base):
    """Organization context persisted by the application when provisioned by an administrator."""

    __tablename__ = "organizations"

    id: str = Column(String(36), primary_key=True)
    name: str = Column(String(160), nullable=False)
    industry: str | None = Column(String(120), nullable=True)
    workplace_type: str | None = Column(String(80), nullable=True)
    configuration: dict = Column(JSON, nullable=False, default=dict)
