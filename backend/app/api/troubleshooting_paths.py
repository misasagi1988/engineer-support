from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.troubleshooting_path import TroubleshootingPath
from app.schemas.troubleshooting_path import (
    TroubleshootingPathCreate,
    TroubleshootingPathUpdate,
    TroubleshootingPathResponse,
)

router = APIRouter(prefix="/troubleshooting-paths", tags=["troubleshooting-paths"])


@router.get("", response_model=list[TroubleshootingPathResponse])
async def list_troubleshooting_paths(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TroubleshootingPath))
    return result.scalars().all()


@router.post("", response_model=TroubleshootingPathResponse, status_code=201)
async def create_troubleshooting_path(data: TroubleshootingPathCreate, db: AsyncSession = Depends(get_db)):
    path = TroubleshootingPath(**data.model_dump(), created_by="admin")
    db.add(path)
    await db.commit()
    await db.refresh(path)
    return path


@router.put("/{path_id}", response_model=TroubleshootingPathResponse)
async def update_troubleshooting_path(
    path_id: str, data: TroubleshootingPathUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(TroubleshootingPath).where(TroubleshootingPath.id == path_id))
    path = result.scalar_one_or_none()
    if not path:
        raise HTTPException(status_code=404, detail="Troubleshooting path not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(path, key, value)
    await db.commit()
    await db.refresh(path)
    return path
