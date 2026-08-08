from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db.session import get_db
from ...schemas.user import UserCreate, UserRead, UserPatch
from ...services.user_service import UserService
from ..dependencies.deps import get_user_service
from ...api.dependencies.auth_deps import get_current_user
from ...models.user import User

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead)
def create_user(data: UserCreate, service: UserService = Depends(get_user_service), db: Session = Depends(get_db)):
    try:
        return service.create_user(data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/me", response_model=UserRead)
def me(current_user: User = Depends(get_current_user), service: UserService = Depends(get_user_service), db: Session = Depends(get_db)):
    user = service.get_user(current_user.id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/", response_model=UserPatch)
def edit_user(data: UserPatch, current_user: User = Depends(get_current_user), service: UserService = Depends(get_user_service), db: Session = Depends(get_db)):
    try:
        user = service.edit_user(current_user.id, data, db)
        if not user:
            raise HTTPException(status_code=404, detail="Invlid user ID")
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
