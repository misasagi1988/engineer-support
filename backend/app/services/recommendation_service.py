from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.case import Case


async def recommend_cases(
    db: AsyncSession,
    module_id: str | None = None,
    deploy_mode: str | None = None,
    keywords: str | None = None,
    limit: int = 5,
) -> list[dict]:
    query = select(Case).where(Case.review_status != "draft")
    if module_id:
        query = query.where(Case.module_id == module_id)
    if deploy_mode:
        query = query.where(Case.deploy_mode == deploy_mode)
    if keywords:
        for kw in keywords.split():
            query = query.where(
                Case.title.contains(kw)
                | Case.root_cause.contains(kw)
                | Case.solution.contains(kw)
            )
    query = query.order_by(Case.confidence_score.desc(), Case.created_at.desc()).limit(limit)
    result = await db.execute(query)
    cases = result.scalars().all()
    return [
        {
            "id": c.id,
            "title": c.title,
            "module_id": c.module_id,
            "deploy_mode": c.deploy_mode,
            "root_cause": c.root_cause,
            "solution": c.solution,
            "confidence_score": c.confidence_score,
        }
        for c in cases
    ]


async def generate_case_draft(
    db: AsyncSession, ticket_id: str, solution: str, root_cause: str
) -> dict:
    return {
        "title": f"Auto-generated case for ticket {ticket_id[:8]}",
        "root_cause": root_cause,
        "solution": solution,
        "tags": [],
    }
