from pydantic import BaseModel
from typing import List, Optional

class Reflectometer(BaseModel):
    id: int | None = None
    name: str
    password: Optional[str] = None

class Participant(BaseModel):
    id: int | None = None
    name: str

    reflectometer: int

class Curve(BaseModel):
    data: List[int]
    
    reflectometer: int

class Response(BaseModel):
    what : str
    when : str
    thoughts : str
    feelings : str
    actions : str
    consequences : str

    reflectometer : int
    curve : int