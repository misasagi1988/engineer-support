from datetime import datetime
from pydantic import BaseModel

class DeploymentBase(BaseModel):
    name: str
    deploy_mode: str
    environment: str = "production"
    config_summary: dict = {}

class DeploymentCreate(DeploymentBase):
    customer_id: str
    version_id: str | None = None

class DeploymentUpdate(BaseModel):
    name: str | None = None
    deploy_mode: str | None = None
    version_id: str | None = None
    environment: str | None = None
    config_summary: dict | None = None

class DeploymentResponse(DeploymentBase):
    id: str
    customer_id: str
    version_id: str | None = None
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
