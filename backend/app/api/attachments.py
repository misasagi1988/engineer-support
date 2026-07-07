from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.db.session import get_db
from app.schemas.attachment import AttachmentResponse

router = APIRouter(prefix="/tickets/{ticket_id}/attachments", tags=["attachments"])


@router.post("/", response_model=AttachmentResponse)
async def upload_attachment(
    ticket_id: str, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)
):
    content = await file.read()
    return AttachmentResponse(
        id=f"stub-{ticket_id}",
        ticket_id=ticket_id,
        case_id=None,
        file_name=file.filename or "unknown",
        file_type="other",
        file_size=len(content),
        storage_path=f"./storage/attachments/{ticket_id}/{file.filename}",
        description="",
        uploaded_by="system",
        created_at=datetime.utcnow(),
    )


@router.get("/")
async def list_attachments(ticket_id: str, db: AsyncSession = Depends(get_db)):
    return []


@router.get("/{attachment_id}")
async def download_attachment(attachment_id: str):
    raise HTTPException(status_code=501, detail="Not implemented in MVP")


@router.delete("/{attachment_id}")
async def delete_attachment(attachment_id: str):
    return {"status": "ok"}
