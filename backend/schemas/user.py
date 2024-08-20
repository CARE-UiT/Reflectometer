from pydantic import BaseModel


class NewUser(BaseModel):
    user_name: str
    email: str
    password : str | None
    class Config:
        from_attributes = True

class User(BaseModel):
    id: int
    user_name: str
    email: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None