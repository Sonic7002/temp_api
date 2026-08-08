from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
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
    data: str = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(require_role(UserRole.TEACHER)),
    db: Session = Depends(get_db),
    note_service: NoteService = Depends(get_note_service),
    classroom_service: ClassroomService = Depends(get_classroom_service),
):
    try:
        notes_data = NotesCreate.model_validate_json(data)

        return note_service.create_notes(
            notes_data,
            db,
            file
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=list[NotesRead])
def list_notes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    note_service: NoteService = Depends(get_note_service)
):
    """List all notes."""
    return note_service.get_all(db)

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

@router.get("/{note_id}")
def get_note_url(note_id: UUID, current_user: User = Depends(get_current_user), service: NoteService = Depends(get_note_service), db: Session = Depends(get_db)):
    try:
        return service.get_note_url(note_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{note_id}", response_model=NotesRead)
def delete_file(note_id: UUID, current_user: User = Depends(get_current_user), service: NoteService = Depends(get_note_service), db: Session = Depends(get_db)):
    try:
        doc = service.delete_note(note_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return doc
