from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.dependencies.auth_deps import get_current_user
from app.api.dependencies.rbac import require_role
from app.api.dependencies.deps import get_assessment_service, get_attempt_service, get_quiz_service
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserRole
from app.schemas.assessment import AssessmentCreate, AssessmentRead, State
from app.services.assessment_service import AssessmentService
from app.services.attempt_service import AttemptService
from app.services.quiz_service import QuizService

router = APIRouter(prefix="/assessments", tags=["assessments"])

class SubmitAnswerRequest(BaseModel):
    attempt_id: UUID
    question_id: UUID
    submitted_answer: str

@router.post("/", response_model=AssessmentRead, status_code=status.HTTP_201_CREATED)
def submit_question_response(
    payload: SubmitAnswerRequest,
    current_user: User = Depends(require_role(UserRole.STUDENT)),
    db: Session = Depends(get_db),
    assessment_service: AssessmentService = Depends(get_assessment_service),
    attempt_service: AttemptService = Depends(get_attempt_service),
    quiz_service: QuizService = Depends(get_quiz_service)
):
    """Students answer questions one by one. Evaluates answer and stores response status in assessment table."""
    attempt = attempt_service.get_by_id(attempt_id=payload.attempt_id, db=db)
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attempt not found"
        )
    if attempt.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only submit responses for your own attempt"
        )
        
    quiz = quiz_service.get_by_id(quiz_id=payload.question_id, db=db)
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz question not found"
        )
        
    is_correct = payload.submitted_answer.strip().upper() == quiz.answer.strip().upper()
    assessment_status = State.CORRECT if is_correct else State.INCORRECT

    assessment_data = AssessmentCreate(
        attempt_id=payload.attempt_id,
        question_id=payload.question_id,
        status=assessment_status
    )

    assessment = assessment_service.create_assessment(data=assessment_data, db=db)
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to record question assessment"
        )

    return assessment

@router.get("/attempt/{attempt_id}", response_model=list[AssessmentRead])
def get_assessments_for_attempt(
    attempt_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    assessment_service: AssessmentService = Depends(get_assessment_service),
    attempt_service: AttemptService = Depends(get_attempt_service)
):
    """View responses/assessments recorded for a specific attempt."""
    attempt = attempt_service.get_by_id(attempt_id=attempt_id, db=db)
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attempt not found"
        )

    if current_user.role == UserRole.STUDENT.value and attempt.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this attempt assessment"
        )

    assessments = assessment_service.get_by_attempt_id(attempt_id=attempt_id, db=db)
    return assessments or []
