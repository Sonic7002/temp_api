from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..models.quiz import Quiz
from ..schemas.quiz import QuizCreate

class QuizRepo:
    def create(self, db: Session, data: QuizCreate) -> Quiz | None:
        quiz = Quiz(
            note_id = data.note_id,
            question = data.question,
            opA = data.opA,
            opB = data.opB,
            opC = data.opC,
            opD = data.opD,
            answer = data.answer,
            difficulty = data.difficulty
        )
        try:
            db.add(quiz)
            db.commit()
            db.refresh(quiz)
            return quiz
        except IntegrityError:
            return None

    def get_by_id(self, db: Session, quiz_id: UUID) -> Quiz | None:
        return db.query(Quiz).filter(Quiz.id == str(quiz_id)).first()

    def get_by_note_id(self, db: Session, note_id: UUID) -> list[Quiz]:
        return db.query(Quiz).filter(Quiz.note_id == str(note_id)).all()

    def get_by_note_ids(self, db: Session, note_ids: list[UUID]) -> list[Quiz]:
        string_ids = [str(nid) for nid in note_ids]
        return db.query(Quiz).filter(Quiz.note_id.in_(string_ids)).all()
        
    def list_all(self, db: Session) -> list[Quiz]:
        return db.query(Quiz).all()

    def save(self, db: Session, note: Quiz) -> Quiz:
        try:
            db.commit()
            db.refresh(note)
            return note
        except IntegrityError:
            raise ValueError("conflict in database rules")

    def delete(self, db: Session, quiz_id: UUID) -> Quiz | None:
        quiz = self.get_by_id(db, quiz_id)
        if quiz:
            db.delete(quiz)
            db.commit()
        return quiz
