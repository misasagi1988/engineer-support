from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.case import Case
from app.schemas.case import CaseCreate

async def create_case(db: AsyncSession, data: CaseCreate, created_by: str) -> Case:
    case = Case(**data.model_dump(), created_by=created_by)
    db.add(case)
    await db.commit()
    await db.refresh(case)
    return case

async def get_case(db: AsyncSession, case_id: str) -> Case | None:
    result = await db.execute(select(Case).where(Case.id == case_id))
    return result.scalar_one_or_none()

async def list_cases(db: AsyncSession, module_id: str | None = None, deploy_mode: str | None = None, review_status: str | None = None, search: str | None = None, skip: int = 0, limit: int = 20) -> list[Case]:
    query = select(Case)
    if module_id: query = query.where(Case.module_id == module_id)
    if deploy_mode: query = query.where(Case.deploy_mode == deploy_mode)
    if review_status: query = query.where(Case.review_status == review_status)
    if search: query = query.where(Case.title.contains(search) | Case.root_cause.contains(search) | Case.solution.contains(search))
    query = query.offset(skip).limit(limit).order_by(Case.created_at.desc())
    result = await db.execute(query)
    return list(result.scalars().all())

async def review_case(db: AsyncSession, case: Case, review_status: str, reviewed_by: str) -> Case:
    case.review_status = review_status
    case.reviewed_by = reviewed_by
    return case
