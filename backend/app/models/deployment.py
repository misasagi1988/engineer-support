import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Enum as SAEnum, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Deployment(Base):
    __tablename__ = "deployments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id: Mapped[str] = mapped_column(String(36), ForeignKey("customers.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    deploy_mode: Mapped[str] = mapped_column(SAEnum("standalone", "ha", "cluster", "hierarchical"), nullable=False)
    version_id: Mapped[str] = mapped_column(String(36), ForeignKey("versions.id"), nullable=True)
    environment: Mapped[str] = mapped_column(SAEnum("production", "staging", "test"), default="production")
    config_summary: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
