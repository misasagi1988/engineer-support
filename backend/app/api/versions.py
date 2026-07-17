from fastapi import APIRouter, Depends
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import get_current_user_id
from app.db.session import get_db
from app.models.version import Version
from app.schemas.version import VersionCreate, VersionResponse

router = APIRouter(prefix="/versions", tags=["versions"])


@router.get("", response_model=list[VersionResponse])
async def list_versions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Version).order_by(desc(Version.name)))
    return result.scalars().all()


@router.post("", response_model=VersionResponse, status_code=201)
async def create_version(data: VersionCreate, db: AsyncSession = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    version = Version(**data.model_dump())
    db.add(version)
    await db.commit()
    await db.refresh(version)
    return version
