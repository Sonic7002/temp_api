from uuid import UUID
from sqlalchemy.orm import Session
from ..models.attempt import Attempt
from ..repos.attempt_repo import AttemptRepo
from ..schemas.attempt import AttemptCreate

class AttemptService:
    def __init__(self, repo: AttemptRepo):
        self.repo = repo

    def create_attempt(self, user_id: UUID, data: AttemptCreate, db: Session) -> Attempt | None:
        return self.repo.create(db, user_id, data)

    def get_by_id(self, attempt_id: UUID, db: Session) -> Attempt | None:
        return self.repo.get_by_id(db, attempt_id)

    def get_by_user_id(self, user_id: UUID, db: Session) -> list[Attempt] | None:
        return self.repo.get_by_user_id(db, user_id)

    def get_all(self, db: Session) -> list[Attempt]:
        return self.repo.list_all(db)
