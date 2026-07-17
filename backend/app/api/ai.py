from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import get_current_user_id
from app.db.session import get_db
from app.models.module import Module
from app.models.version import Version
from app.models.troubleshooting_path import TroubleshootingPath
from app.schemas.ai import AILocateRequest, AILocateResponse
from app.services.llm_service import analyze_problem
from app.services.recommendation_service import recommend_cases

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/locate", response_model=AILocateResponse)
async def ai_locate(data: AILocateRequest, db: AsyncSession = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    modules_result = await db.execute(select(Module.name))
    modules = [r[0] for r in modules_result.all()]

    versions_result = await db.execute(select(Version.name))
    versions = [r[0] for r in versions_result.all()]

    ai_result = await analyze_problem(data.description, modules, versions)

    matched_module = ai_result["module_candidates"][0]["module"] if ai_result["module_candidates"] else None

    module_id = None
    if matched_module:
        m_result = await db.execute(select(Module).where(Module.name == matched_module))
        m = m_result.scalar_one_or_none()
        if m:
            module_id = m.id

    cases = await recommend_cases(
        db, module_id=module_id, deploy_mode=data.deploy_mode, keywords=data.description, limit=5
    )

    tp_query = select(TroubleshootingPath)
    if module_id:
        tp_query = tp_query.where(TroubleshootingPath.module_id == module_id)
    if data.deploy_mode:
        tp_query = tp_query.where(TroubleshootingPath.deploy_mode == data.deploy_mode)
    tp_result = await db.execute(tp_query)
    tp = tp_result.scalars().first()
    # Fallback: if no deploy_mode-specific path found, try "all"
    if not tp and module_id:
        fallback_query = select(TroubleshootingPath).where(
            TroubleshootingPath.module_id == module_id,
            TroubleshootingPath.deploy_mode == "all",
        )
        fallback_result = await db.execute(fallback_query)
        tp = fallback_result.scalars().first()
    steps = tp.steps if tp else []

    return AILocateResponse(
        module_candidates=ai_result.get("module_candidates", []),
        version_candidates=ai_result.get("version_candidates", []),
        deploy_mode_hints=ai_result.get("deploy_mode_hints"),
        root_cause_candidates=ai_result.get("root_cause_candidates", []),
        similar_cases=cases,
        troubleshooting_path=steps,
    )


@router.get("/troubleshooting-path/{module_id}")
async def get_troubleshooting_path(
    module_id: str,
    deploy_mode: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    query = select(TroubleshootingPath).where(TroubleshootingPath.module_id == module_id)
    if deploy_mode:
        query = query.where(TroubleshootingPath.deploy_mode == deploy_mode)
    result = await db.execute(query.order_by(TroubleshootingPath.deploy_mode))
    path = result.scalars().first()
    # Fallback to "all" if deploy_mode-specific path not found
    if not path and deploy_mode:
        fallback_query = select(TroubleshootingPath).where(
            TroubleshootingPath.module_id == module_id,
            TroubleshootingPath.deploy_mode == "all",
        )
        fallback_result = await db.execute(fallback_query)
        path = fallback_result.scalars().first()
    return {"steps": path.steps if path else []}
