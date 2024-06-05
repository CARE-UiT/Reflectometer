from typing import Any, Optional
from models import Course
from sqlalchemy.orm import Session

def create_course(session: Session, name: str, owner: int, password_hash: Optional[str] = None, salt: Optional[str] = None) -> None:
    new_course = Course(name=name, owner=owner, password_hash=password_hash, salt=salt)
    session.add(new_course)
    session.commit()

def get_course(session: Session, course_id: int) -> Optional[Course]:
    return session.query(Course).filter_by(id=course_id).first()

def update_course(session: Session, course_id: int, **kwargs: Any) -> None:
    course = session.query(Course).filter_by(id=course_id).first()
    if course:
        for key, value in kwargs.items():
            setattr(course, key, value)
        session.commit()

def delete_course(session: Session, course_id: int) -> None:
    course = session.query(Course).filter_by(id=course_id).first()
    if course:
        session.delete(course)
        session.commit()
