from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.customers import router as customers_router
from app.api.deployments import router as deployments_router
from app.api.tickets import router as tickets_router
from app.api.cases import router as cases_router
from app.api.modules import router as modules_router
from app.api.versions import router as versions_router
from app.api.attachments import router as attachments_router
from app.api.troubleshooting_paths import router as troubleshooting_paths_router
from app.api.ai import router as ai_router
from app.api.stats import router as stats_router

api_router = APIRouter()
for r in [
    auth_router,
    users_router,
    customers_router,
    deployments_router,
    tickets_router,
    cases_router,
    modules_router,
    versions_router,
    attachments_router,
    troubleshooting_paths_router,
    ai_router,
    stats_router,
]:
    api_router.include_router(r)
