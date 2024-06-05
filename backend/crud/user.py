from typing import Any, Optional
from models import User
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

def create_user(session: Session, user_name: str, email: str, password_hash: str, salt: str) -> None:
    new_user = User(user_name=user_name, email=email, password_hash=password_hash, salt=salt)
    session.add(new_user)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        print("User with this username or email already exists.")

def get_user(session: Session, user_id: int) -> Optional[User]:
    return session.query(User).filter_by(id=user_id).first()

def update_user(session: Session, user_id: int, **kwargs: Any) -> None:
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        for key, value in kwargs.items():
            setattr(user, key, value) #This can fail due to use of Any type
        session.commit()

def delete_user(session: Session, user_id: int) -> None:
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        session.delete(user)
        session.commit()
