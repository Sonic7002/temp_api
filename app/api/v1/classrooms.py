from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth_deps import get_current_user
from app.api.dependencies.rbac import require_role
from app.api.dependencies.deps import get_classroom_service
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserRole
from app.schemas.classroom import ClassroomCreate, ClassroomRead
from app.services.classroom_service import ClassroomService

router = APIRouter(prefix="/classrooms", tags=["classrooms"])

@router.post("/", response_model=ClassroomRead, status_code=status.HTTP_201_CREATED)
def create_classroom(
    data: ClassroomCreate,
    current_user: User = Depends(require_role(UserRole.TEACHER)),
    db: Session = Depends(get_db),
    classroom_service: ClassroomService = Depends(get_classroom_service)
):
    """Only teacher users can create classrooms."""
    classroom = classroom_service.create_classroom(user_id=current_user.id, data=data, db=db)
    if not classroom:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create classroom"
        )
    return classroom

@router.get("/my-classrooms", response_model=list[ClassroomRead])
def get_my_created_classrooms(
    current_user: User = Depends(require_role(UserRole.TEACHER)),
    db: Session = Depends(get_db),
    classroom_service: ClassroomService = Depends(get_classroom_service)
):
    """Special endpoint for teachers to view their created classrooms."""
    classrooms = classroom_service.get_by_user(user_id=current_user.id, db=db)
    return classrooms or []

@router.post("/{classroom_id}/join")
def join_classroom(
    classroom_id: UUID,
    current_user: User = Depends(require_role(UserRole.STUDENT)),
    db: Session = Depends(get_db),
    classroom_service: ClassroomService = Depends(get_classroom_service)
):
    """Any student can join any classroom."""
    classroom = classroom_service.get_by_id(classroom_id=classroom_id, db=db)
    if not classroom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Classroom not found"
        )
    return {
        "message": f"Successfully joined classroom '{classroom.title}'",
        "classroom_id": classroom.id,
        "student_id": current_user.id
    }

@router.get("/", response_model=list[ClassroomRead])
def list_classrooms(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    classroom_service: ClassroomService = Depends(get_classroom_service)
):
    """All classrooms are visible to all authenticated users."""
    return classroom_service.get_all(db=db)

@router.get("/{classroom_id}", response_model=ClassroomRead)
def get_classroom(
    classroom_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    classroom_service: ClassroomService = Depends(get_classroom_service)
):
    """Get classroom by ID for any authenticated user."""
    classroom = classroom_service.get_by_id(classroom_id=classroom_id, db=db)
    if not classroom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Classroom not found"
        )
    return classroom
