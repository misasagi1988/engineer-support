from datetime import datetime
from typing import Literal
from pydantic import BaseModel, field_validator

VALID_STATUSES = {"pending", "processing", "resolved", "closed"}
VALID_SOURCES = {"jira", "wechat", "manual"}
VALID_PRIORITIES = {"p0", "p1", "p2", "p3"}

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

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        if v not in VALID_STATUSES:
            raise ValueError(f"status must be one of {VALID_STATUSES}, got '{v}'")
        return v

    @field_validator("source")
    @classmethod
    def validate_source(cls, v: str) -> str:
        if v not in VALID_SOURCES:
            raise ValueError(f"source must be one of {VALID_SOURCES}, got '{v}'")
        return v

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, v: str) -> str:
        if v not in VALID_PRIORITIES:
            raise ValueError(f"priority must be one of {VALID_PRIORITIES}, got '{v}'")
        return v

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
    status: Literal["pending", "processing", "resolved", "closed"]
    solution: str | None = None

class TicketResponse(BaseModel):
    """Read-only schema — no validators, so list serialization is O(N) without per-row set lookups."""
    id: str
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
    identified_root_cause: str = ""
    solution: str = ""
    troubleshooting_checklist: list = []
    auto_identified: bool = False
    created_at: datetime
    resolved_at: datetime | None = None
    updated_at: datetime
    class Config:
        from_attributes = True
