from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID

class CurveBase(BaseModel):
    session: UUID = Field(..., description="Session ID associated with the curve")
    participant: Optional[int] = Field(None, description="Participant ID associated with the curve")

class CurveCreate(CurveBase):
    data: List[float] = Field(..., description="List of curve data points")

class CurveUpdate(CurveBase):
    id: int
    data: List[float] = Field(None, description="List of curve data points")  # Optional for updates

class Curve(CurveBase):
    id: int
    data: List[float] = Field(..., description="List of curve data points")

    class Config:
        orm_mode = True

class CurveGet(CurveBase):
    id: int

    class Config:
        orm_mode = True
