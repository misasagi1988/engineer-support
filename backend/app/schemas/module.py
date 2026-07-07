from datetime import datetime
from pydantic import BaseModel

class ModuleBase(BaseModel):
    name: str
    description: str = ""

class ModuleCreate(ModuleBase): pass

class ModuleUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

class ModuleResponse(ModuleBase):
    id: str
    created_at: datetime
    class Config:
        from_attributes = True
