from ..repos.note_repo import NoteRepo
from uuid import UUID
from sqlalchemy.orm import Session
from ..schemas.note import NotesCreate, NotesPatch
from ..models.note import Note

class NoteService:
    def __init__(self, repo: NoteRepo):
        self.repo = repo

    def create_notes(self, data: NotesCreate, db: Session) -> Note:
        return self.repo.create(db, data)

    def get_by_id(self, note_id: UUID, db: Session) -> Note | None:
        return self.repo.get_by_id(db, note_id)

    def get_by_class_id(self, class_id: UUID, db: Session) -> Note | None:
        return self.repo.get_by_class_id(db, class_id)

    def get_all(self, db: Session) -> list[Note]:
        return self.repo.list_all(db)

    def update_note(self, note_id: UUID, data: NotesPatch, db: Session) -> Note:
        note = self.get_by_id(note_id, db)

        if not note:
            raise ValueError("Note not found")

        updates = data.model_dump(exclude_unset=True)

        for field, value in updates.items():
            setattr(note, field, value)

        return self.repo.save(db, note)

    def delete_note(self, note_id: UUID, db: Session):
        note = self.get_by_id(note_id, db)

        if not note:
            raise ValueError("Note not found")
                
        self.repo.delete(db, note_id)

        return note