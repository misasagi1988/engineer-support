from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import get_current_user_id, require_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.case import CaseCreate, CaseUpdate, CaseReview, CaseResponse
from app.services import case_service

router = APIRouter(prefix="/cases", tags=["cases"])


@router.get("", response_model=list[CaseResponse])
async def list_cases(
    module_id: str | None = Query(None),
    deploy_mode: str | None = Query(None),
    review_status: str | None = Query(None),
    search: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    return await case_service.list_cases(
        db,
        module_id=module_id,
        deploy_mode=deploy_mode,
        review_status=review_status,
        search=search,
        skip=skip,
        limit=limit,
    )


@router.post("", response_model=CaseResponse, status_code=201)
async def create_case(data: CaseCreate, db: AsyncSession = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    return await case_service.create_case(db, data, created_by=user_id)


@router.get("/{case_id}", response_model=CaseResponse)
async def get_case(case_id: str, db: AsyncSession = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    case = await case_service.get_case(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@router.put("/{case_id}", response_model=CaseResponse)
async def update_case(case_id: str, data: CaseUpdate, db: AsyncSession = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    case = await case_service.get_case(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(case, key, value)
    await db.commit()
    await db.refresh(case)
    return case


@router.put("/{case_id}/review", response_model=CaseResponse)
async def review_case(case_id: str, data: CaseReview, db: AsyncSession = Depends(get_db), user: User = Depends(require_admin)):
    case = await case_service.get_case(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    await case_service.review_case(db, case, data.review_status, reviewed_by=user.id)
    await db.commit()
    await db.refresh(case)
    return case


@router.post("/search", response_model=list[CaseResponse])
async def search_cases(query: str, db: AsyncSession = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    return await case_service.list_cases(db, search=query, limit=20)
