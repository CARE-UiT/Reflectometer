from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import date as datetype
from .curve import CurveGet
class SessionBase(BaseModel):
    name: str = Field(..., example="Session Name")

class SessionCreate(SessionBase):
    course: int = Field(..., example="1")  # Required course_id to associate with a course

class SessionUpdate(SessionBase):
    name: Optional[str] = Field(None, example="New Session Name")

class Session(SessionBase):
    id: UUID  # UUID4 for the primary key
    course: int
    responses: List[int] = []  # List of response IDs
    curves: List[CurveGet] = []  # List of curve IDs

    class Config:
        orm_mode = True

class SessionCheck(SessionBase):
    id: UUID  # UUID4 for the primary key

    class Config:
        orm_mode = True