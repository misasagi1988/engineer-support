from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.case import Case
from app.models.module import Module
from app.services.llm_service import generate_case_from_ticket


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
    db: AsyncSession,
    ticket,
) -> dict:
    """Generate a case draft from a resolved ticket using LLM.

    Calls the LLM to produce structured case content, falling back to
    raw ticket fields when the LLM is unavailable.
    """
    module_name = ""
    if ticket.module_id:
        m_result = await db.execute(select(Module).where(Module.id == ticket.module_id))
        m = m_result.scalar_one_or_none()
        if m:
            module_name = m.name

    llm_result = await generate_case_from_ticket(
        description=ticket.description or "",
        root_cause=ticket.identified_root_cause or "",
        solution=ticket.solution or "",
        module_name=module_name,
    )

    return {
        "title": llm_result["title"],
        "root_cause": llm_result["root_cause"],
        "solution": llm_result["solution"],
        "troubleshooting_path": llm_result.get("troubleshooting_path", []),
        "tags": llm_result.get("tags", []),
        "ticket_id": ticket.id,
        "module_id": ticket.module_id,
        "deploy_mode": ticket.deploy_mode,
    }
