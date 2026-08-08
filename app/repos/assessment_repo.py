from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..models.assessment import Assessment
from ..schemas.assessment import AssessmentCreate

class AssessmentRepo:
    def create(self, db: Session, data: AssessmentCreate) -> Assessment | None:
        assessment = Assessment(attempt_id = data.attempt_id, quiz_id = data.question_id, status = data.status)
        try:
            db.add(assessment)
            db.commit()
            db.refresh(assessment)
            return assessment
        except IntegrityError:
            return None

    def get_by_id(self, db: Session, assessment_id: UUID) -> Assessment | None:
        return db.query(Assessment).filter(Assessment.id == str(assessment_id)).first()

    def get_by_attempt_id(self, db: Session, attempt_id: UUID) -> list[Assessment]:
        return db.query(Assessment).filter(Assessment.attempt_id == str(attempt_id)).all()
        
    def list_all(self, db: Session) -> list[Assessment]:
        return db.query(Assessment).all()

    def save(self, db: Session, assessment: Assessment) -> Assessment:
        try:
            db.commit()
            db.refresh(assessment)
            return assessment
        except IntegrityError:
            raise ValueError("conflict in database rules")
