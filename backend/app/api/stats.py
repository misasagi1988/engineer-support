from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import get_current_user_id
from app.db.session import get_db
from app.services.stats_service import get_dashboard_stats

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/dashboard")
async def dashboard(db: AsyncSession = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    return await get_dashboard_stats(db)
