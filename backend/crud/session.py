from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from models import Session as SessionModel, Course as CourseModel
import schemas

def create_session(db: Session, session_data: schemas.SessionCreate, user_id: int) -> SessionModel:
    # Check course ownership
    course = db.query(CourseModel).filter(CourseModel.id == session_data.course, CourseModel.owner == user_id).first()
    if not course:
        raise HTTPException(status_code=403, detail="Not authorized to create a session for this course")

    new_session = SessionModel(**session_data.model_dump())
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

def check_session(db: Session, session_id: UUID) -> SessionModel:
    return db.query(SessionModel).filter(SessionModel.id==session_id).first()

def get_session(db: Session, session_id: UUID, user_id: int) -> SessionModel:
    return db.query(SessionModel).join(CourseModel).filter(SessionModel.id == session_id, CourseModel.owner == user_id).first()

def get_sessions_by_course(db: Session, course: int, user_id: int) -> list[SessionModel]:
    return db.query(SessionModel).join(CourseModel).filter(SessionModel.course == course, CourseModel.owner == user_id).all()

def update_session(db: Session, session_id: UUID, session_data: schemas.SessionUpdate, user_id: int) -> SessionModel:
    session = db.query(SessionModel).join(CourseModel).filter(SessionModel.id == session_id, CourseModel.owner == user_id).first()
    if not session:
        return None
    for key, value in session_data.model_dump(exclude_unset=True).items():
        setattr(session, key, value)
    db.commit()
    db.refresh(session)
    return session

def delete_session(db: Session, session_id: UUID, user_id: int) -> None:
    session = db.query(SessionModel).join(CourseModel).filter(SessionModel.id == session_id, CourseModel.owner == user_id).first()
    if session:
        db.delete(session)
        db.commit()
