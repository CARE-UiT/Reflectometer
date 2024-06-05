from typing import Any, Optional
from models import Curve
from sqlalchemy.orm import Session

def create_curve(session: Session, data: bytes, session_id: int, participant: int) -> None:
    new_curve = Curve(data=data, session=session_id, participant=participant)
    session.add(new_curve)
    session.commit()

def get_curve(session: Session, curve_id: int) -> Optional[Curve]:
    return session.query(Curve).filter_by(id=curve_id).first()

def update_curve(session: Session, curve_id: int, **kwargs: Any) -> None:
    curve = session.query(Curve).filter_by(id=curve_id).first()
    if curve:
        for key, value in kwargs.items():
            setattr(curve, key, value)
        session.commit()

def delete_curve(session: Session, curve_id: int) -> None:
    curve = session.query(Curve).filter_by(id=curve_id).first()
    if curve:
        session.delete(curve)
        session.commit()
