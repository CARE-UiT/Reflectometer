from typing import Any, Optional
from models import Session as SessionModel
from sqlalchemy.orm import Session

def create_session(session: Session, name: str, course: int, password_hash: Optional[str] = None, salt: Optional[str] = None) -> None:
    new_session = SessionModel(name=name, course=course, password_hash=password_hash, salt=salt)
    session.add(new_session)
    session.commit()

def get_session_by_id(session: Session, session_id: int) -> Optional[Session]:
    return session.query(SessionModel).filter_by(id=session_id).first()

def update_session(session: Session, session_id: int, **kwargs: Any) -> None:
    session_obj = session.query(SessionModel).filter_by(id=session_id).first()
    if session_obj:
        for key, value in kwargs.items():
            setattr(session_obj, key, value)
        session.commit()

def delete_session(session: Session, session_id: int) -> None:
    session_obj = session.query(SessionModel).filter_by(id=session_id).first()
    if session_obj:
        session.delete(session_obj)
        session.commit()
