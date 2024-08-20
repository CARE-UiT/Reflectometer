from uuid import UUID
from sqlalchemy.orm import Session
from models import Session as SessionModel, Course as CourseModel
from fastapi import HTTPException

def check_course_ownership(db: Session, session_id: UUID, user_id: int) -> None:
    # Fetch the session and course related to the session ID
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    course = db.query(CourseModel).filter(CourseModel.id == session.course).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Ensure the current user is the owner of the course
    if course.owner != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
