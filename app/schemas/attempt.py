from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class AttemptCreate(BaseModel):
    notes_id: list[UUID]

class AttemptRead(BaseModel):
    id: UUID
    notes_id: list[UUID]
    created_at: datetime
