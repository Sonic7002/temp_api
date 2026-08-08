from uuid import uuid4, UUID as PyUUID
from datetime import datetime
from sqlalchemy import String, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from ..db.base import Base

class Assessment(Base):
    __tablename__ = "assessments"

    id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    attempt_id: Mapped[PyUUID] = mapped_column(ForeignKey("attempts.id"), nullable=False)
    quiz_id: Mapped[PyUUID] = mapped_column(ForeignKey("quizes.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(300), nullable=False)

    quiz = relationship("Quiz")
    attempt = relationship("Attempt")
