from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
    user_name: str
    email: str
    password : str | None
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_name: str | None = None

class Reflectometer(BaseModel):
    id: int | None = None
    name: str
    password: Optional[str] = None

class Participant(BaseModel):
    id: int | None = None
    name: str

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