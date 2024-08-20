from sqlalchemy.orm import Session
from models import KeyMoment as KeyMomentModel, Session as SessionModel, Course as CourseModel
import models
import schemas
from fastapi import HTTPException
from .utils import check_course_ownership  # Import the helper method

# Create a new KeyMoment (any user with session_id)
def create_keymoment(db: Session, keymoment_data: schemas.KeyMomentCreate) -> KeyMomentModel:
    new_keymoment = KeyMomentModel(
        xvalue=keymoment_data.xvalue,
        yvalue=keymoment_data.yvalue,
        what=keymoment_data.what,
        when=keymoment_data.when,
        thoughts=keymoment_data.thoughts,
        feelings=keymoment_data.feelings,
        actions=keymoment_data.actions,
        consequences=keymoment_data.consequences,
        session=keymoment_data.session,
        participant=keymoment_data.participant,
        curve=keymoment_data.curve
    )
    db.add(new_keymoment)
    db.commit()
    db.refresh(new_keymoment)
    return new_keymoment

# Get key moments by curves (Only course owner)
def get_keymoments_by_curve(db: Session, curve_id: int, user_id):
    keymoments = db.query(KeyMomentModel).filter(KeyMomentModel.curve == curve_id).all()
    if len(keymoments) > 0:
        check_course_ownership(db,keymoments[0].session, user_id)
    return keymoments

# Get a KeyMoment (only course owner)
def get_keymoment(db: Session, keymoment_id: int, user_id: int) -> KeyMomentModel:
    keymoment = db.query(KeyMomentModel).filter(KeyMomentModel.id == keymoment_id).first()
    if not keymoment:
        raise HTTPException(status_code=404, detail="KeyMoment not found")

    # Check if the user is the owner of the course related to the key moment's session
    check_course_ownership(db, keymoment.session, user_id)

    return keymoment

# Update a KeyMoment (only course owner)
def update_keymoment(db: Session, keymoment_id: int, keymoment_data: schemas.KeyMomentUpdate, user_id: int) -> KeyMomentModel:
    keymoment = db.query(KeyMomentModel).filter(KeyMomentModel.id == keymoment_id).first()
    if not keymoment:
        raise HTTPException(status_code=404, detail="KeyMoment not found")

    # Check if the user is the owner of the course related to the key moment's session
    check_course_ownership(db, keymoment.session, user_id)

    # Update the key moment data
    for field, value in keymoment_data.dict(exclude_unset=True).items():
        setattr(keymoment, field, value)

    db.commit()
    db.refresh(keymoment)
    return keymoment

# Delete a KeyMoment (only course owner)
def delete_keymoment(db: Session, keymoment_id: int, user_id: int) -> None:
    keymoment = db.query(KeyMomentModel).filter(KeyMomentModel.id == keymoment_id).first()
    if not keymoment:
        raise HTTPException(status_code=404, detail="KeyMoment not found")

    # Check if the user is the owner of the course related to the key moment's session
    check_course_ownership(db, keymoment.session, user_id)

    db.delete(keymoment)
    db.commit()
