from typing import Any, Optional
from models import Participant
from sqlalchemy.orm import Session

def create_participant(session: Session, name: str, course: int) -> None:
    new_participant = Participant(name=name, course=course)
    session.add(new_participant)
    session.commit()

def get_participant(session: Session, participant_id: int) -> Optional[Participant]:
    return session.query(Participant).filter_by(id=participant_id).first()

def update_participant(session: Session, participant_id: int, **kwargs: Any) -> None:
    participant = session.query(Participant).filter_by(id=participant_id).first()
    if participant:
        for key, value in kwargs.items():
            setattr(participant, key, value)
        session.commit()

def delete_participant(session: Session, participant_id: int) -> None:
    participant = session.query(Participant).filter_by(id=participant_id).first()
    if participant:
        session.delete(participant)
        session.commit()
