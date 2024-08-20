from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import schemas
import crud
from database import get_db
from auth import get_current_user

router = APIRouter()

@router.get("/sessions/{session_id}/curves", response_model=List[schemas.Curve], tags=["Session", "Curve"])
async def get_curves_by_session(
    session_id: UUID,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    sessions = crud.get_curves_by_session(db, session_id, current_user.id)
    return sessions

@router.post("/curves", response_model=schemas.Curve, tags=["Curve"])
async def create_curve(
    curve_data: schemas.CurveCreate,
    db: Session = Depends(get_db),
):
    new_curve = crud.create_curve(db, curve_data)
    return new_curve

@router.get("/curves/{curve_id}", response_model=schemas.Curve, tags=["Curve"])
async def get_curve(
    curve_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    curve = crud.get_curve(db, curve_id, current_user.id)
    return curve

@router.put("/curves/{curve_id}", response_model=schemas.Curve, tags=["Curve"])
async def update_curve(
    curve_id: int,
    curve_data: schemas.CurveUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    updated_curve = crud.update_curve(db, curve_id, curve_data, current_user.id)
    return updated_curve

@router.delete("/curves/{curve_id}", tags=["Curve"])
async def delete_curve(
    curve_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    crud.delete_curve(db, curve_id, current_user.id)
    return {"detail": "Curve deleted"}
