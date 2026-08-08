from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from enum import Enum


class State(str, Enum):
    CORRECT = "CORRECT"
    INCORRECT = "INCORRECT"

class AssessmentCreate(BaseModel):
    attempt_id: UUID
    question_id: UUID
    status: State

class AssessmentRead(BaseModel):
    id: UUID
    attempt_id: UUID
    question_id: UUID
    status: State
