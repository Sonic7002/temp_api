from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth_deps import get_current_user
from app.api.dependencies.rbac import require_role
from app.api.dependencies.deps import get_quiz_service, get_note_service
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserRole
from app.schemas.quiz import QuizCreate, QuizPatch, QuizRead
from app.services.quiz_service import QuizService
from app.services.notes_service import NoteService

router = APIRouter(prefix="/quizzes", tags=["quizzes"])

@router.post("/", response_model=QuizRead, status_code=status.HTTP_201_CREATED)
def create_quiz(
    data: QuizCreate,
    current_user: User = Depends(require_role(UserRole.TEACHER)),
    db: Session = Depends(get_db),
    quiz_service: QuizService = Depends(get_quiz_service),
    note_service: NoteService = Depends(get_note_service)
):
    """Teachers can upload quizzes for a particular note."""
    note = note_service.get_by_id(note_id=data.note_id, db=db)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    quiz = quiz_service.create_quiz(data=data, db=db)
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create quiz"
        )
    return quiz

@router.patch("/{quiz_id}", response_model=QuizRead)
def update_quiz(
    quiz_id: UUID,
    data: QuizPatch,
    current_user: User = Depends(require_role(UserRole.TEACHER)),
    db: Session = Depends(get_db),
    quiz_service: QuizService = Depends(get_quiz_service)
):
    """Teachers can edit quizzes."""
    try:
        updated_quiz = quiz_service.update_quiz(quiz_id=quiz_id, data=data, db=db)
        return updated_quiz
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )

@router.delete("/{quiz_id}", response_model=QuizRead)
def delete_quiz(
    quiz_id: UUID,
    current_user: User = Depends(require_role(UserRole.TEACHER)),
    db: Session = Depends(get_db),
    quiz_service: QuizService = Depends(get_quiz_service)
):
    """Teachers can delete quizzes."""
    try:
        deleted_quiz = quiz_service.delete_quiz(quiz_id=quiz_id, db=db)
        return deleted_quiz
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )

@router.get("/note/{note_id}", response_model=list[QuizRead])
def get_quizzes_by_note(
    note_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    quiz_service: QuizService = Depends(get_quiz_service)
):
    """Get all quizzes created for a specific note."""
    quizzes = quiz_service.get_by_note_id(note_id=note_id, db=db)
    return quizzes or []

@router.get("/{quiz_id}", response_model=QuizRead)
def get_quiz(
    quiz_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    quiz_service: QuizService = Depends(get_quiz_service)
):
    """Get quiz details by ID."""
    quiz = quiz_service.get_by_id(quiz_id=quiz_id, db=db)
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    return quiz
