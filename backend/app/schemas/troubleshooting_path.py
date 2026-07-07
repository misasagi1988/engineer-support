from datetime import datetime
from pydantic import BaseModel

class TroubleshootingPathBase(BaseModel):
    module_id: str
    deploy_mode: str = "all"
    steps: list = []
    version: str = "1.0"

class TroubleshootingPathCreate(TroubleshootingPathBase): pass

class TroubleshootingPathUpdate(BaseModel):
    deploy_mode: str | None = None
    steps: list | None = None
    version: str | None = None

class TroubleshootingPathResponse(TroubleshootingPathBase):
    id: str
    created_by: str
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
