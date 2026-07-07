import uuid
from datetime import datetime

from sqlalchemy import String, Text, Enum as SAEnum, Boolean, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    external_id: Mapped[str] = mapped_column(String(100), nullable=True)
    customer_id: Mapped[str] = mapped_column(String(36), ForeignKey("customers.id"), nullable=True)
    deployment_id: Mapped[str] = mapped_column(String(36), ForeignKey("deployments.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    module_id: Mapped[str] = mapped_column(String(36), ForeignKey("modules.id"), nullable=True)
    version_id: Mapped[str] = mapped_column(String(36), ForeignKey("versions.id"), nullable=True)
    deploy_mode: Mapped[str] = mapped_column(SAEnum("standalone", "ha", "cluster", "hierarchical"), nullable=True)
    source: Mapped[str] = mapped_column(SAEnum("jira", "wechat", "manual"), default="manual")
    status: Mapped[str] = mapped_column(SAEnum("pending", "processing", "resolved", "closed"), default="pending")
    priority: Mapped[str] = mapped_column(SAEnum("p0", "p1", "p2", "p3"), default="p2")
    assignee_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=True)
    identified_root_cause: Mapped[str] = mapped_column(Text, default="")
    solution: Mapped[str] = mapped_column(Text, default="")
    troubleshooting_checklist: Mapped[list] = mapped_column(JSON, default=list)
    auto_identified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    resolved_at: Mapped[datetime] = mapped_column(nullable=True)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
