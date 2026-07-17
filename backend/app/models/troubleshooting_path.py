import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Enum as SAEnum, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class TroubleshootingPath(Base):
    __tablename__ = "troubleshooting_paths"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    module_id: Mapped[str] = mapped_column(String(36), ForeignKey("modules.id"), nullable=False)
    deploy_mode: Mapped[str] = mapped_column(SAEnum("all", "standalone", "ha", "cluster", "hierarchical"), default="all")
    steps: Mapped[list] = mapped_column(JSON, default=list)
    version: Mapped[str] = mapped_column(String(20), default="1.0")
    created_by: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
