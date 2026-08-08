from uuid import UUID
from pydantic import EmailStr
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..models.user import User
from ..schemas.user import UserCreate

class UserRepo:
    def create(self, db: Session, data: UserCreate) -> User | None:
        user = User(name = data.name, email = data.email, role = data.role)
        user.set_password(data.password)
        try:
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except IntegrityError:
            return None

    def get_by_id(self, db: Session, user_id: UUID) ->  User | None:
        return db.query(User).filter(User.id == str(user_id)).first()

    def get_by_email(self, db: Session, email: EmailStr) -> User | None:
        return db.query(User).filter(User.email == email).first()

    def list_all(self, db: Session) -> list[User]:
        return db.query(User).all()

    def save(self, db: Session, user: User) -> User:
        try:
            db.commit()
            db.refresh(user)
            return user
        except IntegrityError:
            raise ValueError("email already exists")
