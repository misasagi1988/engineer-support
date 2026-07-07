from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "operator"


class UserUpdate(BaseModel):
    email: str | None = None
    role: str | None = None
