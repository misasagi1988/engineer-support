import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.attachment import Attachment

# Mapping from file extension to attachment type
FILE_TYPE_MAP = {
    ".log": "log",
    ".txt": "log",
    ".gz": "log",
    ".yaml": "config",
    ".yml": "config",
    ".json": "config",
    ".conf": "config",
    ".xml": "config",
    ".ini": "config",
    ".png": "screenshot",
    ".jpg": "screenshot",
    ".jpeg": "screenshot",
    ".gif": "screenshot",
    ".webp": "screenshot",
    ".bmp": "screenshot",
}


def _infer_file_type(filename: str) -> str:
    ext = Path(filename).suffix.lower()
    return FILE_TYPE_MAP.get(ext, "other")


def _storage_path(ticket_id: str, filename: str) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    safe_name = f"{timestamp}_{filename}"
    return str(Path(settings.ATTACHMENT_STORAGE_PATH) / ticket_id / safe_name)


async def upload_attachment(
    db: AsyncSession,
    ticket_id: str,
    file: UploadFile,
    description: str,
    uploaded_by: str,
) -> Attachment:
    content = await file.read()
    file_size = len(content)
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if file_size > max_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Max size: {settings.MAX_UPLOAD_SIZE_MB}MB",
        )

    filename = file.filename or "unknown"
    file_type = _infer_file_type(filename)
    storage = _storage_path(ticket_id, filename)

    # Ensure directory exists
    os.makedirs(os.path.dirname(storage), exist_ok=True)
    with open(storage, "wb") as f:
        f.write(content)

    attachment = Attachment(
        id=str(uuid.uuid4()),
        ticket_id=ticket_id,
        case_id=None,
        file_name=filename,
        file_type=file_type,
        file_size=file_size,
        storage_path=storage,
        description=description,
        uploaded_by=uploaded_by,
        created_at=datetime.now(timezone.utc),
    )
    db.add(attachment)
    await db.commit()
    await db.refresh(attachment)
    return attachment


async def list_attachments(db: AsyncSession, ticket_id: str) -> list[Attachment]:
    result = await db.execute(
        select(Attachment).where(Attachment.ticket_id == ticket_id).order_by(Attachment.created_at.desc())
    )
    return list(result.scalars().all())


async def get_attachment(db: AsyncSession, attachment_id: str) -> Attachment | None:
    result = await db.execute(select(Attachment).where(Attachment.id == attachment_id))
    return result.scalar_one_or_none()


async def delete_attachment(db: AsyncSession, attachment_id: str) -> bool:
    attachment = await get_attachment(db, attachment_id)
    if not attachment:
        return False
    # Delete physical file
    if os.path.exists(attachment.storage_path):
        os.remove(attachment.storage_path)
    await db.delete(attachment)
    await db.commit()
    return True
