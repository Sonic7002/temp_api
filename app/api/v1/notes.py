from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth_deps import get_current_user
from app.api.dependencies.rbac import require_role
from app.api.dependencies.deps import get_note_service, get_classroom_service
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserRole
from app.schemas.note import NotesCreate, NotesRead
from app.services.notes_service import NoteService
from app.services.classroom_service import ClassroomService

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("/", response_model=NotesRead, status_code=status.HTTP_201_CREATED)
def upload_note(
    data: NotesCreate,
    current_user: User = Depends(require_role(UserRole.TEACHER)),
    db: Session = Depends(get_db),
    note_service: NoteService = Depends(get_note_service),
    classroom_service: ClassroomService = Depends(get_classroom_service)
):
    """Any teacher can upload any note in any class."""
    classroom = classroom_service.get_by_id(classroom_id=data.class_id, db=db)
    if not classroom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Classroom not found"
        )
    note = note_service.create_notes(data=data, db=db)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to upload note"
        )
    return note

@router.get("/", response_model=list[NotesRead])
def list_notes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    note_service: NoteService = Depends(get_note_service)
):
    """List all notes."""
    return note_service.get_all(db=db)

@router.get("/class/{class_id}", response_model=list[NotesRead])
def get_notes_by_class(
    class_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    note_service: NoteService = Depends(get_note_service)
):
    """Get all notes for a specific classroom."""
    notes = note_service.get_by_class_id(class_id=class_id, db=db)
    return notes or []

@router.get("/{note_id}", response_model=NotesRead)
def get_note(
    note_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    note_service: NoteService = Depends(get_note_service)
):
    """Get note details by ID."""
    note = note_service.get_by_id(note_id=note_id, db=db)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    return note
