from pydantic import BaseModel
from datetime import datetime


class ProjectCreate(BaseModel):
    code: str | None = None
    name: str
    investor_name: str | None = None


class ProjectResponse(BaseModel):
    id: str
    code: str | None = None
    name: str
    investor_name: str | None = None
    created_at: datetime