from pydantic import BaseModel


class AILocateRequest(BaseModel):
    description: str
    module_id: str | None = None
    deploy_mode: str | None = None


class AILocateResponse(BaseModel):
    module_candidates: list[dict] = []
    version_candidates: list[dict] = []
    deploy_mode_hints: str | None = None
    root_cause_candidates: list[dict] = []
    similar_cases: list[dict] = []
    troubleshooting_path: list[dict] = []
