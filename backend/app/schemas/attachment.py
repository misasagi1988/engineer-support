from datetime import datetime
from pydantic import BaseModel

class AttachmentResponse(BaseModel):
    id: str
    ticket_id: str
    case_id: str | None = None
    file_name: str
    file_type: str
    file_size: int
    storage_path: str
    description: str
    uploaded_by: str
    created_at: datetime
    class Config:
        from_attributes = True
