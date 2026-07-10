import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Text, Enum as SAEnum, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Attachment(Base):
    __tablename__ = "attachments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    ticket_id: Mapped[str] = mapped_column(String(36), ForeignKey("tickets.id"), nullable=False)
    case_id: Mapped[str] = mapped_column(String(36), ForeignKey("cases.id"), nullable=True)
    file_name: Mapped[str] = mapped_column(String(500), nullable=False)
    file_type: Mapped[str] = mapped_column(SAEnum("log", "config", "screenshot", "other"), default="other")
    file_size: Mapped[int] = mapped_column(BigInteger, default=0)
    storage_path: Mapped[str] = mapped_column(String(1000), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    uploaded_by: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
