from pydantic import BaseModel

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