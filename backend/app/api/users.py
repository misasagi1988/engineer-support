from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import get_current_user_id, require_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.auth_service import hash_password

router = APIRouter(prefix="/users", tags=["users"])


@router.get("")
async def list_users(db: AsyncSession = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return [
        {"id": u.id, "username": u.username, "role": u.role}
        for u in users
    ]


@router.post("", status_code=201)
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db), _admin: User = Depends(require_admin)):
    # Check if username already exists
    existing = await db.execute(select(User).where(User.username == data.username))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Username already exists")
    user = User(
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password),
        role=data.role,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"id": user.id, "username": user.username, "role": user.role, "email": user.email}


@router.put("/{user_id}/role")
async def update_user_role(user_id: str, data: UserUpdate, db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user_id)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if data.role:
        user.role = data.role
    await db.commit()
    return {"id": user.id, "role": user.role}
