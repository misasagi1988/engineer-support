import uuid
from datetime import datetime

from sqlalchemy import String, Text, Enum as SAEnum, Float, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Case(Base):
    __tablename__ = "cases"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    ticket_id: Mapped[str] = mapped_column(String(36), ForeignKey("tickets.id"), nullable=False)
    customer_id: Mapped[str] = mapped_column(String(36), ForeignKey("customers.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    module_id: Mapped[str] = mapped_column(String(36), ForeignKey("modules.id"), nullable=False)
    deploy_mode: Mapped[str] = mapped_column(SAEnum("standalone", "ha", "cluster", "hierarchical"), nullable=True)
    root_cause: Mapped[str] = mapped_column(Text, default="")
    solution: Mapped[str] = mapped_column(Text, default="")
    troubleshooting_path: Mapped[dict] = mapped_column(JSON, default=list)
    tags: Mapped[dict] = mapped_column(JSON, default=list)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0)
    review_status: Mapped[str] = mapped_column(SAEnum("draft", "reviewed", "archived"), default="draft")
    reviewed_by: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=True)
    created_by: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
