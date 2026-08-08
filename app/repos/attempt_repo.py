from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..models.attempt import Attempt
from ..schemas.attempt import AttemptCreate

class AttemptRepo:
    def create(self, db: Session, user_id: UUID, data: AttemptCreate) -> Attempt | None:
        attempt = Attempt(user_id = user_id, notes_id = data.notes_id)
        try:
            db.add()
            db.commit()
            db.refresh(attempt)
            return attempt
        except IntegrityError:
            return None

    def get_by_id(self, db: Session, attempt_id: UUID) -> Attempt | None:
        return db.query(Attempt).filter(Attempt.id == str(attempt_id)).first()

    def get_by_user_id(self, db: Session, user_id: UUID) -> list[Attempt] | None:
        return db.query(Attempt).filter(Attempt.user_id == str(user_id)).all()
        
    def list_all(self, db: Session) -> list[Attempt]:
        return db.query(Attempt).all()

    def save(self, db: Session, attepmt: Attempt) -> Attempt:
        try:
            db.commit()
            db.refresh(Attempt)
            return Attempt
        except IntegrityError:
            raise ValueError("conflict in database rules")
