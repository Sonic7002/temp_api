from ..repos.classroom_repo import ClassRepo
from uuid import UUID
from sqlalchemy.orm import Session
from ..schemas.classroom import ClassroomCreate, ClassroomPatch
from ..models.classroom import Classroom

class ClassroomService:
    def __init__(self, repo: ClassRepo):
        self.repo = repo

    def create_classroom(self, user_id: UUID, data: ClassroomCreate, db: Session) -> Classroom:
        return self.repo.create(db, data, user_id)

    def get_by_id(self, classroom_id: UUID, db: Session) -> Classroom | None:
        return self.repo.get_by_id(db, classroom_id)

    def get_by_user(self, user_id: UUID, db: Session) -> Classroom | None:
        return self.repo.get_by_user_id(db, user_id)

    def get_all(self, db: Session) -> list[Classroom]:
        return self.repo.list_all(db)

    def update_classroom(self, user_id: UUID, classroom_id: UUID, data: ClassroomPatch, db: Session) -> Classroom:
        classroom = self.get_by_id(classroom_id, db)

        if not classroom:
            raise ValueError("Classroom not found")

        if classroom.user_id != user_id:
            raise ValueError("Classroom not found")

        updates = data.model_dump(exclude_unset=True)

        for field, value in updates.items():
            setattr(classroom, field, value)

        return self.repo.save(db, classroom)

    def delete_classroom(self, user_id: UUID, classroom_id: UUID, db: Session):
        classroom = self.get_by_id(user_id, db)

        if not classroom:
            raise ValueError("Classroom not found")
        
        if classroom.user_id != user_id:
            raise ValueError("Classroom not found")
                
        self.repo.delete(db, classroom_id)

        return classroom