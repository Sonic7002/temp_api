from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..models.quiz import Quiz
from ..schemas.quiz import QuizCreate

class QuizRepo:
    def create(self, db: Session, data: QuizCreate) -> Quiz | None:
        quiz = Quiz(question = data.question, opA = data.opA, opB = data.opB, opC = data.opC, opD = data.opD, answer = data.answer, difficulty = data.difficulty)
        try:
            db.add()
            db.commit()
            db.refresh()
            return quiz
        except IntegrityError:
            return None

    def get_by_id(self, db: Session, quiz_id: UUID) -> Quiz | None:
        return db.query(Quiz).filter(Quiz.id == str(quiz_id)).first()

    def get_by_note_id(self, db: Session, note_id: UUID) -> list[Quiz] | None:
        return db.query(Quiz).filter(Quiz.note_id == str(note_id)).all()
        
    def list_all(self, db: Session) -> list[Quiz]:
        return db.query(Quiz).all()

    def save(self, db: Session, note: Quiz) -> Quiz:
        try:
            db.commit()
            db.refresh(note)
            return note
        except IntegrityError:
            raise ValueError("conflict in database rules")
