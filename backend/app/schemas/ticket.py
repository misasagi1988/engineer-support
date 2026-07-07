from datetime import datetime
from pydantic import BaseModel

class TicketBase(BaseModel):
    title: str
    description: str = ""
    external_id: str | None = None
    customer_id: str | None = None
    deployment_id: str | None = None
    module_id: str | None = None
    version_id: str | None = None
    deploy_mode: str | None = None
    source: str = "manual"
    status: str = "pending"
    priority: str = "p2"
    assignee_id: str | None = None

class TicketCreate(TicketBase): pass

class TicketUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    module_id: str | None = None
    version_id: str | None = None
    deploy_mode: str | None = None
    assignee_id: str | None = None
    solution: str | None = None
    identified_root_cause: str | None = None

class TicketStatusUpdate(BaseModel):
    status: str

class TicketResponse(TicketBase):
    id: str
    identified_root_cause: str = ""
    solution: str = ""
    troubleshooting_checklist: list = []
    auto_identified: bool = False
    created_at: datetime
    resolved_at: datetime | None = None
    updated_at: datetime
    class Config:
        from_attributes = True
