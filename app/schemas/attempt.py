from pydantic import BaseModel, field_validator, ValidationInfo
from uuid import UUID
from datetime import datetime
from typing import Optional

class AttemptCreate(BaseModel):
    notes_id: list[UUID]

class AttemptRead(BaseModel):
    id: UUID
    notes_id: list[UUID]
    created_at: datetime
