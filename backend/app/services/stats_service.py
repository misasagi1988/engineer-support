from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ticket import Ticket


async def get_dashboard_stats(db: AsyncSession) -> dict:
    # Single query using GROUP BY instead of 4 separate full-table COUNT scans
    result = await db.execute(
        select(Ticket.status, func.count(Ticket.id))
        .group_by(Ticket.status)
    )
    counts = dict(result.all())

    return {
        "total": sum(counts.values()),
        "pending": counts.get("pending", 0),
        "processing": counts.get("processing", 0),
        "resolved": counts.get("resolved", 0),
        "closed": counts.get("closed", 0),
    }
