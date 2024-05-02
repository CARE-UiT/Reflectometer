from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import schema, models
from sqlalchemy.orm import Session
from database import get_db
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import JWTError, jwt
import bcrypt


SECRET_KEY = "6944036b9f42f24c3e63970078e38e90f2878161110563abaf477f5b14f96f25"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 2*60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password, salt):
    return pwd_context.verify(salt+plain_password, hashed_password)

def get_password_hash(password: str, salt: str):
    return pwd_context.hash(salt+password)

def get_db_user(userName: str, db: Session = Depends(get_db)):
    userModel = db.query(models.User).filter(models.User.user_name == userName).first()
    return userModel

def get_user(userName: str, db: Session):
    userModel = db.query(models.User).filter(models.User.user_name == userName).first()
    return schema.User(user_name=userModel.user_name, email=userModel.email, password=None)

def authenticate_user(userName: str, password: str, db: Session):
    user = get_db_user(userName, db)
    if user is None:
        return False
    if not verify_password(password, user.password_hash, user.salt):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schema.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(token_data.username, db)
    if user is None:
        raise credentials_exception
    return user

def create_new_user(newUser: schema.User, db: Session):
    salt = bcrypt.gensalt().decode()
    passwordHash = get_password_hash(newUser.password, salt)
    exists = db.query(models.User).filter(
            models.User.user_name == newUser.user_name).first()
    if exists:
        raise HTTPException(status.HTTP_409_CONFLICT, "User with this name allready exists in our system.")
    else:
        user_model = models.User(
            user_name = newUser.user_name,
            email = newUser.email,
            password_hash = passwordHash,
            salt = salt
        )
        db.add(user_model)
        db.commit()
    return user_model

