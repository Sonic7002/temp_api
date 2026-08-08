from pydantic import BaseModel, field_validator, ValidationInfo
from uuid import UUID
from datetime import datetime
from typing import Optional

class ClassroomCreate(BaseModel):
    title: str

    @field_validator("title")
    @classmethod
    def not_empty(cls, v: str, info: ValidationInfo):
        if not v.strip():
            raise ValueError(f"{info.field_name} must not be empty")
        return v

class ClassroomRead(BaseModel):
    id: UUID
    title: str
    user_id: UUID
    created_at: datetime

class ClassroomPatch(BaseModel):
    title: Optional[str] = None

    @field_validator("title")
    @classmethod
    def not_empty(cls, v: str, info: ValidationInfo):
        if v is None:
            pass 
        elif not v.strip():
            raise ValueError(f"{info.field_name} must not be empty")
        return v