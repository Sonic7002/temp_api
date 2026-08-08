# this file contains authentication dependencies for routes

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError
from app.core.jwt import decode_access_token
from app.db.session import get_db
from app.repos.user_repo import UserRepo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "/auth/login")
user_repo = UserRepo()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """this fuction fetches and returns the user out of a jwt key or raises appropriate error"""
    try:
        payload = decode_access_token(token)
        user_id = payload["sub"]
    except (JWTError, KeyError):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)

    user = user_repo.get_by_id(db, user_id)


    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)

    return user
