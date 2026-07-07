from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, LoginResponse, UserInfo
from app.services.auth_service import create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


def get_current_user_from_token(request: Request) -> dict | None:
    from app.services.auth_service import decode_access_token

    auth_header = request.headers.get("authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    return decode_access_token(auth_header[7:])


@router.post("/login", response_model=LoginResponse)
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == req.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user.id, user.role)
    return LoginResponse(access_token=token)


@router.get("/me", response_model=UserInfo)
async def get_me(request: Request, db: AsyncSession = Depends(get_db)):
    payload = get_current_user_from_token(request)
    if not payload:
        raise HTTPException(status_code=401, detail="Not authenticated")
    result = await db.execute(select(User).where(User.id == payload["sub"]))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return UserInfo(id=user.id, username=user.username, email=user.email, role=user.role)
