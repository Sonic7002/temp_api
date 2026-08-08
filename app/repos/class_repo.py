from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..models.classroom import Classroom
from ..schemas.classroom import ClassroomCreate

class ClassRepo:
    def create(self, db: Session, data: ClassroomCreate, user_id: UUID) -> Classroom | None:
        classroom = Classroom(title = data.title, user_id = user_id)
        try:
            db.add()
            db.commit()
            db.refresh(classroom)
            return classroom
        except IntegrityError:
            return None

    def get_by_id(self, db: Session, classroom_id: UUID) -> Classroom | None:
        return db.query(Classroom).filter(Classroom.id == str(classroom_id)).first()

    def get_by_user_id(self, db: Session, user_id: UUID) -> list[Classroom] | None:
        return db.query(Classroom).filter(Classroom.user_id == str(user_id)).all()
        
    def list_all(self, db: Session) -> list[Classroom]:
        return db.query(Classroom).all()

    def save(self, db: Session, classroom: Classroom) -> Classroom:
        try:
            db.commit()
            db.refresh(classroom)
            return classroom
        except IntegrityError:
            raise ValueError("conflict in database rules")
