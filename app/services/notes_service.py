from uuid import UUID
from pathlib import Path
from fastapi import UploadFile
from sqlalchemy.orm import Session

from ..repos.note_repo import NoteRepo
from ..schemas.note import NotesCreate, NotesPatch
from ..models.note import Note
from ..db.file_client import supabase

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB (increased for MP4 support)
BUCKET_NAME = "temp"

ALLOWED_MIME_TYPES = {
    "application/pdf": ".pdf",
    "video/mp4": ".mp4",
}


class NoteService:
    def __init__(self, repo: NoteRepo):
        self.repo = repo

    def _validate_and_get_extension(self, file: UploadFile) -> str:
        """Validates file type, extension, and size limits."""
        content_type = file.content_type
        if content_type not in ALLOWED_MIME_TYPES:
            raise ValueError("Only PDF and MP4 files are allowed")

        ext = Path(file.filename or "").suffix.lower()
        expected_ext = ALLOWED_MIME_TYPES[content_type]
        if ext != expected_ext:
            raise ValueError(f"Invalid file extension. Expected {expected_ext}")

        if file.size and file.size > MAX_FILE_SIZE:
            raise ValueError("File size exceeds 50MB limit")

        return expected_ext

    def create_notes(self, data: NotesCreate, db: Session, file: UploadFile | None = None) -> Note:
        # 1. Create DB record to generate unique ID
        note = self.repo.create(db, data)
        if not note:
            return None

        if file:
            # 2. Validate file format before storage upload
            ext = self._validate_and_get_extension(file)
            storage_key = f"{note.id}{ext}"

            # 3. Upload file to Supabase storage
            try:
                file_bytes = file.file.read()
                if len(file_bytes) > MAX_FILE_SIZE:
                    raise ValueError("File content exceeds 50MB limit")

                supabase.storage.from_(BUCKET_NAME).upload(
                    path=storage_key,
                    file=file_bytes,
                    file_options={"content-type": file.content_type}
                )
                note.file_extension = ext
                return self.repo.save(db, note)
            except Exception as err:
                # Clean up repo state if storage upload fails
                self.repo.delete(db, note.id)
                db.rollback()
                raise ValueError(f"File upload failed: {err}") from err

        return note

    def get_by_id(self, note_id: UUID, db: Session) -> Note | None:
        return self.repo.get_by_id(db, note_id)

    def get_by_class_id(self, class_id: UUID, db: Session) -> Note | None:
        return self.repo.get_by_class_id(db, class_id)

    def get_all(self, db: Session) -> list[Note]:
        return self.repo.list_all(db)

    def get_note_url(self, note_id: UUID, db: Session) -> dict:
        """Generates a public or signed access URL for the note's media file."""
        note = self.get_by_id(note_id, db)
        if not note:
            raise ValueError("Note not found")

        ext = getattr(note, "file_extension", ".pdf")
        storage_key = f"{note.id}{ext}"

        try:
            file_url = supabase.storage.from_(BUCKET_NAME).get_public_url(storage_key)
        except Exception as err:
            raise ValueError(f"Could not generate access URL: {err}") from err

        return {
            "note_id": note.id,
            "title": note.title,
            "file_url": file_url,
        }

    def update_note(
        self,
        note_id: UUID,
        data: NotesPatch,
        db: Session,
        file: UploadFile | None = None
    ) -> Note:
        note = self.get_by_id(note_id, db)
        if not note:
            raise ValueError("Note not found")

        # Handle optional new file upload
        if file:
            ext = self._validate_and_get_extension(file)
            old_ext = getattr(note, "file_extension", ".pdf")
            old_storage_key = f"{note.id}{old_ext}"
            new_storage_key = f"{note.id}{ext}"

            try:
                # Remove old file if format changed (e.g. PDF replaced with MP4)
                if old_ext != ext:
                    supabase.storage.from_(BUCKET_NAME).remove([old_storage_key])

                file_bytes = file.file.read()
                supabase.storage.from_(BUCKET_NAME).upload(
                    path=new_storage_key,
                    file=file_bytes,
                    file_options={"content-type": file.content_type, "upsert": "true"}
                )
                note.file_extension = ext
            except Exception as err:
                db.rollback()
                raise ValueError(f"File update failed: {err}") from err

        # Apply schema updates
        updates = data.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(note, field, value)

        return self.repo.save(db, note)

    def delete_note(self, note_id: UUID, db: Session) -> Note:
        note = self.get_by_id(note_id, db)
        if not note:
            raise ValueError("Note not found")

        # 1. Clean up file from Supabase storage
        ext = getattr(note, "file_extension", ".pdf")
        storage_key = f"{note.id}{ext}"
        supabase.storage.from_(BUCKET_NAME).remove([storage_key])

        # 2. Delete database record
        self.repo.delete(db, note_id)
        return note