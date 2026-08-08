from app.repos.user_repo import UserRepo
from app.repos.classroom_repo import ClassRepo
from app.repos.note_repo import NoteRepo
from app.repos.quiz_repo import QuizRepo
from app.repos.attempt_repo import AttemptRepo
from app.repos.assessment_repo import AssessmentRepo

from app.services.user_service import UserService
from app.services.classroom_service import ClassroomService
from app.services.notes_service import NoteService
from app.services.quiz_service import QuizService
from app.services.attempt_service import AttemptService
from app.services.assessment_service import AssessmentService

# Instantiate repository singletons
user_repo = UserRepo()
classroom_repo = ClassRepo()
note_repo = NoteRepo()
quiz_repo = QuizRepo()
attempt_repo = AttemptRepo()
assessment_repo = AssessmentRepo()

def get_user_service() -> UserService:
    return UserService(repo=user_repo)

def get_classroom_service() -> ClassroomService:
    return ClassroomService(repo=classroom_repo)

def get_note_service() -> NoteService:
    return NoteService(repo=note_repo)

def get_quiz_service() -> QuizService:
    return QuizService(repo=quiz_repo)

def get_attempt_service() -> AttemptService:
    return AttemptService(repo=attempt_repo)

def get_assessment_service() -> AssessmentService:
    return AssessmentService(repo=assessment_repo)
