from uuid import UUID
from sqlalchemy.orm import Session
from ..models.quiz import Quiz
from ..repos.quiz_repo import QuizRepo
from ..schemas.quiz import QuizCreate, QuizPatch

class QuizService:
    def __init__(self, repo: QuizRepo):
        self.repo = repo

    def create_quiz(self, data: QuizCreate, db: Session) -> Quiz | None:
        return self.repo.create(db, data)

    def get_by_id(self, quiz_id: UUID, db: Session) -> Quiz | None:
        return self.repo.get_by_id(db, quiz_id)

    def get_by_note_id(self, note_id: UUID, db: Session) -> list[Quiz] | None:
        return self.repo.get_by_note_id(db, note_id)

    def get_all(self, db: Session) -> list[Quiz]:
        return self.repo.list_all(db)

    def update_quiz(self, quiz_id: UUID, data: QuizPatch, db: Session) -> Quiz:
        quiz = self.get_by_id(quiz_id, db)
        if not quiz:
            raise ValueError("Quiz not found")

        updates = data.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(quiz, field, value)

        return self.repo.save(db, quiz)

    def delete_quiz(self, quiz_id: UUID, db: Session) -> Quiz:
        quiz = self.get_by_id(quiz_id, db)
        if not quiz:
            raise ValueError("Quiz not found")
        self.repo.delete(db, quiz_id)
        return quiz

    def get_quizzes_for_notes(self, note_ids: list[UUID], db: Session, limit: int = 10) -> list[Quiz]:
        quizzes = self.repo.get_by_note_ids(db, note_ids)
        return quizzes[:limit]
