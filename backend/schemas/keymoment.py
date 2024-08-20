from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class KeyMomentBase(BaseModel):
    xvalue: float = Field(..., description="X coordinate of the key moment")
    yvalue: float = Field(..., description="Y coordinate of the key moment")
    what: Optional[str] = Field(None, description="What happened")
    when: Optional[str] = Field(None, description="When did it happen")
    thoughts: Optional[str] = Field(None, description="What did you think")
    feelings: Optional[str] = Field(None, description="What did you feel")
    actions: Optional[str] = Field(None, description="What did you do")
    consequences: Optional[str] = Field(None, description="Were there any consequences")
    session: UUID = Field(..., description="Session ID associated with the key moment")
    participant: Optional[int] = Field(None, description="Participant ID associated with the key moment")
    curve: int = Field(..., description="Curve ID associated with the key moment")

class KeyMomentCreate(KeyMomentBase):
    pass

class KeyMomentUpdate(KeyMomentBase):
    xvalue: Optional[int] = Field(None, description="X coordinate of the key moment")
    yvalue: Optional[int] = Field(None, description="Y coordinate of the key moment")

class KeyMoment(KeyMomentBase):
    id: int

    class Config:
        orm_mode = True
