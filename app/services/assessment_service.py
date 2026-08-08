from uuid import UUID
from sqlalchemy.orm import Session
from ..models.assessment import Assessment
from ..repos.assessment_repo import AssessmentRepo
from ..schemas.assessment import AssessmentCreate

class AssessmentService:
    def __init__(self, repo: AssessmentRepo):
        self.repo = repo

    def create_assessment(self, data: AssessmentCreate, db: Session) -> Assessment | None:
        return self.repo.create(db, data)

    def get_by_id(self, assessment_id: UUID, db: Session) -> Assessment | None:
        return self.repo.get_by_id(db, assessment_id)

    def get_by_attempt_id(self, attempt_id: UUID, db: Session) -> list[Assessment] | None:
        return self.repo.get_by_attempt_id(db, attempt_id)

    def get_all(self, db: Session) -> list[Assessment]:
        return self.repo.list_all(db)
