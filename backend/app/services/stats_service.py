from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ticket import Ticket


async def get_dashboard_stats(db: AsyncSession) -> dict:
    total = await db.execute(select(func.count(Ticket.id)))
    pending = await db.execute(select(func.count(Ticket.id)).where(Ticket.status == "pending"))
    processing = await db.execute(select(func.count(Ticket.id)).where(Ticket.status == "processing"))
    resolved = await db.execute(select(func.count(Ticket.id)).where(Ticket.status == "resolved"))
    return {
        "total": total.scalar(),
        "pending": pending.scalar(),
        "processing": processing.scalar(),
        "resolved": resolved.scalar(),
    }
