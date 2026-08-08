from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.dependencies.auth_deps import get_current_user
from app.api.dependencies.rbac import require_role
from app.api.dependencies.deps import get_attempt_service, get_quiz_service
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserRole
from app.schemas.attempt import AttemptCreate, AttemptRead
from app.schemas.quiz import QuizRead
from app.services.attempt_service import AttemptService
from app.services.quiz_service import QuizService

router = APIRouter(prefix="/attempts", tags=["attempts"])

class AttemptResponse(BaseModel):
    attempt: AttemptRead
    total_questions: int
    questions: list[QuizRead]

@router.post("/", response_model=AttemptResponse, status_code=status.HTTP_201_CREATED)
def start_quiz_attempt(
    data: AttemptCreate,
    current_user: User = Depends(require_role(UserRole.STUDENT)),
    db: Session = Depends(get_db),
    attempt_service: AttemptService = Depends(get_attempt_service),
    quiz_service: QuizService = Depends(get_quiz_service)
):
    """Students can start a quiz attempt from selected notes. Retrieves 10 questions for the attempt."""
    if not data.notes_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one note_id must be provided to start an attempt"
        )
        
    attempt = attempt_service.create_attempt(user_id=current_user.id, data=data, db=db)
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to record quiz attempt"
        )
        
    questions = quiz_service.get_quizzes_for_notes(note_ids=data.notes_id, db=db, limit=10)
    
    return AttemptResponse(
        attempt=attempt,
        total_questions=len(questions),
        questions=questions
    )

@router.get("/", response_model=list[AttemptRead])
def list_student_attempts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    attempt_service: AttemptService = Depends(get_attempt_service)
):
    """Get attempts. Students see their own attempts; teachers see all attempts."""
    if current_user.role == UserRole.STUDENT.value:
        attempts = attempt_service.get_by_user_id(user_id=current_user.id, db=db)
        return attempts or []
    return attempt_service.get_all(db=db)

@router.get("/{attempt_id}", response_model=AttemptRead)
def get_attempt_details(
    attempt_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    attempt_service: AttemptService = Depends(get_attempt_service)
):
    """Get attempt details by ID."""
    attempt = attempt_service.get_by_id(attempt_id=attempt_id, db=db)
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attempt not found"
        )
    return attempt
