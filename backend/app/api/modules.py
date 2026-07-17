from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import get_current_user_id
from app.db.session import get_db
from app.models.module import Module
from app.schemas.module import ModuleCreate, ModuleUpdate, ModuleResponse

router = APIRouter(prefix="/modules", tags=["modules"])


@router.get("", response_model=list[ModuleResponse])
async def list_modules(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Module).order_by(Module.name))
    return result.scalars().all()


@router.post("", response_model=ModuleResponse, status_code=201)
async def create_module(data: ModuleCreate, db: AsyncSession = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    module = Module(**data.model_dump())
    db.add(module)
    await db.commit()
    await db.refresh(module)
    return module


@router.put("/{module_id}", response_model=ModuleResponse)
async def update_module(module_id: str, data: ModuleUpdate, db: AsyncSession = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    result = await db.execute(select(Module).where(Module.id == module_id))
    module = result.scalar_one_or_none()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(module, key, value)
    await db.commit()
    await db.refresh(module)
    return module
