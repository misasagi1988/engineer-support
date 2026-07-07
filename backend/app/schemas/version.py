from datetime import datetime, date
from pydantic import BaseModel

class VersionBase(BaseModel):
    name: str
    release_date: date | None = None
    is_active: bool = True

class VersionCreate(VersionBase): pass

class VersionUpdate(BaseModel):
    name: str | None = None
    release_date: date | None = None
    is_active: bool | None = None

class VersionResponse(VersionBase):
    id: str
    created_at: datetime
    class Config:
        from_attributes = True
