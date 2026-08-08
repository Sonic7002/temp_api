from uuid import UUID
from sqlalchemy.orm import Session
from ..models.user import User
from ..repos.user_repo import UserRepo
from ..schemas.user import UserCreate, UserPatch

class UserService:
    def __init__(self, repo: UserRepo):
        self.repo = repo

    def create_user(self, data: UserCreate, db: Session) -> User:
        user = self.repo.create(db, data)
        if user:
            return user
        raise ValueError("email already exists")

    def get_user(self, user_id: UUID, db: Session) -> User | None:
        return self.repo.get_by_id(db, user_id)

    def edit_user(self, user_id: UUID, data: UserPatch, db: Session) -> User:
        user = self.get_user(user_id, db)
        if not user:
            return None
        updates = data.model_dump(exclude_unset=True)

        if "password" in updates:
            user.set_password(updates.pop("password"))
        for field, value in updates.items():
            setattr(user, field, value)

        return self.repo.save(db, user)
