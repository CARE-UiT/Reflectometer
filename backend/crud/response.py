from typing import Any, Optional
from models import Response
from sqlalchemy.orm import Session

def create_response(session: Session, what: Optional[str], when: Optional[str], thoughts: Optional[str], feelings: Optional[str], actions: Optional[str], consequences: Optional[str], session_id: int, participant: int, curve: int) -> None:
    new_response = Response(
        what=what, when=when, thoughts=thoughts, feelings=feelings,
        actions=actions, consequences=consequences, session=session_id,
        participant=participant, curve=curve)
    session.add(new_response)
    session.commit()

def get_response(session: Session, response_id: int) -> Optional[Response]:
    return session.query(Response).filter_by(id=response_id).first()

def update_response(session: Session, response_id: int, **kwargs: Any) -> None:
    response = session.query(Response).filter_by(id=response_id).first()
    if response:
        for key, value in kwargs.items():
            setattr(response, key, value)
        session.commit()

def delete_response(session: Session, response_id: int) -> None:
    response = session.query(Response).filter_by(id=response_id).first()
    if response:
        session.delete(response)
        session.commit()
