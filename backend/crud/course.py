from typing import Any, List, Optional
from models import Course
from sqlalchemy.orm import Session

import schema
import schemas

def create_course(session: Session, newCourse: schemas.CourseCreate, owner: schemas.user) -> Course:
    print({**newCourse.model_dump(), 'owner' : owner.id})
    new_course = Course(**{**newCourse.model_dump(), 'owner' : owner.id})
    session.add(new_course)
    session.commit()
    session.refresh(new_course)
    return new_course

def get_course(session: Session, course_id: int) -> Optional[Course]:
    return session.query(Course).filter_by(id=course_id).first()

def update_course(session: Session, course_id: int, **kwargs: Any) -> Optional[Course]:
    course = session.query(Course).filter_by(id=course_id).first()
    if course:
        for key, value in kwargs.items():
            setattr(course, key, value)
        session.commit()
        session.refresh(course)
    return course

def delete_course(session: Session, course_id: int) -> None:
    course = session.query(Course).filter_by(id=course_id).first()
    if course:
        session.delete(course)
        session.commit()

def get_courses_by_owner(session: Session, owner_id: int) -> List[Course]:
    return session.query(Course).filter_by(owner=owner_id).all()
