from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import schemas
import crud 
from database import get_db
from auth import get_current_user

router = APIRouter()

# Create a KeyMoment (Anyone with a valid session_id can create)
@router.post("/keymoments", response_model=schemas.KeyMoment, tags=["KeyMoment"])
async def create_keymoment(
    keymoment_data: schemas.KeyMomentCreate,
    db: Session = Depends(get_db),
):
    new_keymoment = crud.create_keymoment(db, keymoment_data)
    return new_keymoment

@router.get("/curves/{curve_id}/keymoments", response_model=List[schemas.KeyMoment], tags=["Keymoment", "Curve"])
async def get_keymoments_by_curve(
    curve_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    keymoments = crud.get_keymoments_by_curve(db, curve_id, current_user.id)
    return keymoments

# Get a KeyMoment (Only course owner can view)
@router.get("/keymoments/{keymoment_id}", response_model=schemas.KeyMoment, tags=["KeyMoment"])
async def get_keymoment(
    keymoment_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    keymoment = crud.get_keymoment(db, keymoment_id, current_user.id)
    if not keymoment:
        raise HTTPException(status_code=404, detail="KeyMoment not found")
    return keymoment

# Update a KeyMoment (Only course owner can update)
@router.put("/keymoments/{keymoment_id}", response_model=schemas.KeyMoment, tags=["KeyMoment"])
async def update_keymoment(
    keymoment_id: int,
    keymoment_data: schemas.KeyMomentUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    updated_keymoment = crud.update_keymoment(db, keymoment_id, keymoment_data, current_user.id)
    if not updated_keymoment:
        raise HTTPException(status_code=404, detail="KeyMoment not found")
    return updated_keymoment

# Delete a KeyMoment (Only course owner can delete)
@router.delete("/keymoments/{keymoment_id}", tags=["KeyMoment"])
async def delete_keymoment(
    keymoment_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    crud.delete_keymoment(db, keymoment_id, current_user.id)
    return {"detail": "KeyMoment deleted"}
