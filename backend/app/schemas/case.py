from datetime import datetime
from pydantic import BaseModel

class CaseBase(BaseModel):
    title: str
    module_id: str
    deploy_mode: str | None = None
    root_cause: str = ""
    solution: str = ""
    troubleshooting_path: list = []
    tags: list = []
    confidence_score: float = 0.0

class CaseCreate(CaseBase):
    ticket_id: str | None = None

class CaseUpdate(BaseModel):
    title: str | None = None
    root_cause: str | None = None
    solution: str | None = None
    troubleshooting_path: list | None = None
    tags: list | None = None

class CaseReview(BaseModel):
    review_status: str

class CaseResponse(CaseBase):
    id: str
    ticket_id: str | None = None
    customer_id: str | None = None
    review_status: str = "draft"
    reviewed_by: str | None = None
    created_by: str
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
