from uuid import uuid4, UUID as PyUUID
from datetime import datetime
from sqlalchemy import String, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from ..db.base import Base

class Attempt(Base):
    __tablename__ = "attempts"

    id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    notes_id: Mapped[list[PyUUID]] = mapped_column(ARRAY(UUID))
    user_id: Mapped[PyUUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User")