from uuid import uuid4, UUID as PyUUID
from datetime import datetime
from sqlalchemy import String, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from ..db.base import Base

class Quiz(Base):
    __tablename__ = "quizes"

    id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    note_id: Mapped[PyUUID] = mapped_column(ForeignKey("notes.id"))
    question: Mapped[str] = mapped_column(String, nullable=False)
    opA: Mapped[str] = mapped_column(String, nullable=False)
    opB: Mapped[str] = mapped_column(String, nullable=False)
    opC: Mapped[str] = mapped_column(String, nullable=False)
    opD: Mapped[str] = mapped_column(String, nullable=False)
    answer: Mapped[str] = mapped_column(String(300), nullable=False)
    difficulty: Mapped[str] = mapped_column(String(300), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    note = relationship("Note")