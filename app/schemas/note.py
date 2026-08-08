from pydantic import BaseModel, field_validator, ValidationInfo
from uuid import UUID
from datetime import datetime
from typing import Optional

class NotesCreate(BaseModel):
    title: str
    class_id: UUID

    @field_validator("title")
    @classmethod
    def not_empty(cls, v: str, info: ValidationInfo):
        if not v.strip():
            raise ValueError(f"{info.field_name} must not be empty")
        return v

class NotesRead(BaseModel):
    id: UUID
    title: str
    created_at: datetime

class NotesPatch(BaseModel):
    title: Optional[str] = None

    @field_validator("title")
    @classmethod
    def not_empty(cls, v: str, info: ValidationInfo):
        if v is None:
            pass 
        elif not v.strip():
            raise ValueError(f"{info.field_name} must not be empty")
        return v