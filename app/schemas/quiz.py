from pydantic import BaseModel, field_validator, ValidationInfo
from enum import Enum
from uuid import UUID
from datetime import datetime
from typing import Optional

class Difficulty(str, Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"

class Answer(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"

class QuizCreate(BaseModel):
    note_id: UUID
    question: str
    opA: str
    opB: str
    opC: str
    opD: str
    answer: Answer
    difficulty: Difficulty

    @field_validator("question", "opA", "opB", "opC", "opD")
    @classmethod
    def not_empty(cls, v: str, info: ValidationInfo):
        if not v.strip():
            raise ValueError(f"{info.field_name} must not be empty")
        return v

class QuizRead(BaseModel):
    id: UUID
    note_id: UUID
    question: str
    opA: str
    opB: str
    opC: str
    opD: str
    answer: Answer
    difficulty: Difficulty
    created_at: datetime

class QuizPatch(BaseModel):
    question: Optional[str] = None
    opA: Optional[str] = None
    opB: Optional[str] = None
    opC: Optional[str] = None
    opD: Optional[str] = None
    answer: Optional[Answer] = None

    @field_validator("question", "opA", "opB", "opC", "opD")
    @classmethod
    def not_empty(cls, v: str, info: ValidationInfo):
        if v is None:
            pass 
        elif not v.strip():
            raise ValueError(f"{info.field_name} must not be empty")
        return v