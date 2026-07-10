from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("")
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return [
        {"id": u.id, "username": u.username, "email": u.email, "role": u.role}
        for u in users
    ]


@router.put("/{user_id}/role")
async def update_user_role(user_id: str, data: UserUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if data.role:
        user.role = data.role
    await db.commit()
    return {"id": user.id, "role": user.role}
