import pickle
from typing import List
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Curve as CurveModel
import schemas
from .utils import check_course_ownership  # Import the helper method

# Create a new Curve (any user with session_id)
def create_curve(db: Session, curve_data: schemas.CurveCreate):
    # Pickle the list of integers before storing them in the database
    print("CURVE DATA:", curve_data.data)
    pickled_data = pickle.dumps(curve_data.data)
    print("PICKLED DATA:", curve_data.data)
    new_curve = CurveModel(
        data=pickled_data,
        session=curve_data.session,
        participant=curve_data.participant
    )
    db.add(new_curve)
    db.commit()
    db.refresh(new_curve)
    
    # Unpickle the data before returning it to match the expected response schema
    new_curve.data = pickle.loads(new_curve.data)
    print("NEW CURVE: ", new_curve)
    
    return new_curve

# Get all curves from a session (only course owner)
def get_curves_by_session(db: Session, session_id: UUID, user_id: int) -> List[CurveModel]:
    check_course_ownership(db, session_id, user_id)

    curves = db.query(CurveModel).filter(CurveModel.session == session_id).all()
    
    for curve in curves:
        curve.data = pickle.loads(curve.data)

    return curves 

# Get a Curve (only course owner)
def get_curve(db: Session, curve_id: int, user_id: int) -> CurveModel:
    curve = db.query(CurveModel).filter(CurveModel.id == curve_id).first()
    if not curve:
        raise HTTPException(status_code=404, detail="Curve not found")

    # Check if the user is the owner of the course related to the curve's session
    check_course_ownership(db, curve.session, user_id)

    # Unpickle the data before returning it to match the expected response schema
    curve.data = pickle.loads(curve.data)
    
    return curve

# Update a Curve (only course owner)
def update_curve(db: Session, curve_id: int, curve_data: schemas.CurveUpdate, user_id: int) -> CurveModel:
    curve = db.query(CurveModel).filter(CurveModel.id == curve_id).first()
    if not curve:
        raise HTTPException(status_code=404, detail="Curve not found")

    # Check if the user is the owner of the course related to the curve's session
    check_course_ownership(db, curve.session, user_id)

    # Update the curve data (pickle if data is provided)
    if curve_data.data is not None:
        curve.data = pickle.dumps(curve_data.data)
    if curve_data.session:
        curve.session = curve_data.session
    if curve_data.participant is not None:
        curve.participant = curve_data.participant

    db.commit()
    db.refresh(curve)
    
    # Unpickle the data before returning it to match the expected response schema
    curve.data = pickle.loads(curve.data)
    
    return curve

# Delete a Curve (only course owner)
def delete_curve(db: Session, curve_id: int, user_id: int) -> None:
    curve = db.query(CurveModel).filter(CurveModel.id == curve_id).first()
    if not curve:
        raise HTTPException(status_code=404, detail="Curve not found")

    # Check if the user is the owner of the course related to the curve's session
    check_course_ownership(db, curve.session, user_id)

    db.delete(curve)
    db.commit()
