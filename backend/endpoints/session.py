from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import schemas
import crud
from database import get_db
from auth import get_current_user

router = APIRouter()


@router.get("/sessions/{session_id}/exists", response_model=schemas.SessionCheck, tags=["Session"])
async def get_session(
    session_id: UUID,
    db: Session = Depends(get_db),
):
    session = crud.check_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    print(session)
    return session

@router.post("/sessions", response_model=schemas.Session, tags=["Session"])
async def create_session(
    session_data: schemas.SessionCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    new_session = crud.create_session(db, session_data, current_user.id)
    return new_session

@router.get("/sessions/{session_id}", response_model=schemas.Session, tags=["Session"])
async def get_session(
    session_id: UUID,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    session = crud.get_session(db, session_id, current_user.id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found or not authorized")
    return session

@router.get("/courses/{course_id}/sessions", response_model=List[schemas.Session], tags=["Session"])
async def get_sessions_by_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    sessions = crud.get_sessions_by_course(db, course_id, current_user.id)
    return sessions

@router.put("/sessions/{session_id}", response_model=schemas.Session, tags=["Session"])
async def update_session(
    session_id: UUID,
    session_data: schemas.SessionUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    updated_session = crud.update_session(db, session_id, session_data, current_user.id)
    if not updated_session:
        raise HTTPException(status_code=404, detail="Session not found or not authorized")
    return updated_session

@router.delete("/sessions/{session_id}", tags=["Session"])
async def delete_session(
    session_id: UUID,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    crud.delete_session(db, session_id, current_user.id)
    return {"detail": "Session deleted"}
