import os
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import get_current_user_id
from app.db.session import get_db
from app.schemas.attachment import AttachmentResponse
from app.services import attachment_service

router = APIRouter(prefix="/tickets/{ticket_id}/attachments", tags=["attachments"])


@router.post("", response_model=AttachmentResponse, status_code=201)
async def upload_attachment(
    ticket_id: str,
    file: UploadFile = File(...),
    description: str = Query(""),
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    return await attachment_service.upload_attachment(
        db, ticket_id, file, description, user_id
    )


@router.get("")
async def list_attachments(ticket_id: str, db: AsyncSession = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    items = await attachment_service.list_attachments(db, ticket_id)
    return [
        AttachmentResponse(
            id=a.id,
            ticket_id=a.ticket_id,
            case_id=a.case_id,
            file_name=a.file_name,
            file_type=a.file_type,
            file_size=a.file_size,
            storage_path=a.storage_path,
            description=a.description,
            uploaded_by=a.uploaded_by,
            created_at=a.created_at,
        )
        for a in items
    ]


@router.get("/{attachment_id}")
async def download_attachment(attachment_id: str, db: AsyncSession = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    attachment = await attachment_service.get_attachment(db, attachment_id)
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    if not os.path.exists(attachment.storage_path):
        raise HTTPException(status_code=404, detail="File not found on disk")
    return FileResponse(attachment.storage_path, filename=attachment.file_name)


@router.delete("/{attachment_id}")
async def delete_attachment(attachment_id: str, db: AsyncSession = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    ok = await attachment_service.delete_attachment(db, attachment_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Attachment not found")
    return {"status": "ok"}
