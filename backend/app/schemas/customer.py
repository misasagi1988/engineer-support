from datetime import datetime
from pydantic import BaseModel

class CustomerBase(BaseModel):
    name: str
    contract_level: str = "standard"
    contact_info: str = ""

class CustomerCreate(CustomerBase): pass

class CustomerUpdate(BaseModel):
    name: str | None = None
    contract_level: str | None = None
    contact_info: str | None = None

class CustomerResponse(CustomerBase):
    id: str
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
