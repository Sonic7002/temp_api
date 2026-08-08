from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..models.note import Note
from ..schemas.note import NotesCreate

class ClassRepo:
    def create(self, db: Session, data: NotesCreate) -> Note | None:
        note = Note(title = data.title, class_id = data.class_id)
        try:
            db.add()
            db.commit()
            db.refresh(note)
            return note
        except IntegrityError:
            return None

    def get_by_id(self, db: Session, note_id: UUID) -> Note | None:
        return db.query(Note).filter(Note.id == str(note_id)).first()

    def get_by_user_id(self, db: Session, classroom_id: UUID) -> list[Note] | None:
        return db.query(Note).filter(Note.class_id == str(classroom_id)).all()
        
    def list_all(self, db: Session) -> list[Note]:
        return db.query(Note).all()

    def save(self, db: Session, note: Note) -> Note:
        try:
            db.commit()
            db.refresh(note)
            return note
        except IntegrityError:
            raise ValueError("conflict in database rules")
