from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.core.jwt import create_access_token
from app.db.session import get_db
from app.repos.user_repo import UserRepo
from app.schemas.auth import Token

router = APIRouter(prefix="/auth", tags=["auth"])
user_repo = UserRepo()

@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_repo.get_by_email(db, form.username)

    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"access_token": create_access_token(user.id)}
