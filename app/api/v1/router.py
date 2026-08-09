from fastapi import APIRouter

from app.api.v1.classrooms import router as classrooms_router
from app.api.v1.notes import router as notes_router
from app.api.v1.quizzes import router as quizzes_router
from app.api.v1.attempts import router as attempts_router
from app.api.v1.assessments import router as assessments_router
from app.api.v1.user import router as user_router
from app.api.v1.auth import router as auth_router

api_v1_router = APIRouter(prefix="/v1")

api_v1_router.include_router(classrooms_router)
api_v1_router.include_router(notes_router)
api_v1_router.include_router(quizzes_router)
# api_v1_router.include_router(attempts_router)
# api_v1_router.include_router(assessments_router)
api_v1_router.include_router(user_router)
