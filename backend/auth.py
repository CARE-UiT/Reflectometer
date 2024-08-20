from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import schemas, models
from sqlalchemy.orm import Session
from database import get_db
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import JWTError, jwt
import bcrypt
from environment import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

def verify_password(plain_password, hashed_password, salt):
    return pwd_context.verify(salt + plain_password, hashed_password)

def get_password_hash(password: str, salt: str):
    return pwd_context.hash(salt + password)

def get_db_user_by_email(email: str, db: Session = Depends(get_db)):
    userModel = db.query(models.User).filter(models.User.email == email).first()
    return userModel

def get_user_by_email(email: str, db: Session):
    userModel = db.query(models.User).filter(models.User.email == email).first()
    return schemas.User(id=userModel.id, user_name=userModel.user_name, email=userModel.email)

def authenticate_user(email: str, password: str, db: Session):
    user = get_db_user_by_email(email, db)
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
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(token_data.email, db)
    if user is None:
        raise credentials_exception
    return user

def create_new_user(newUser: schemas.User, db: Session):
    salt = bcrypt.gensalt().decode()
    passwordHash = get_password_hash(newUser.password, salt)
    exists = db.query(models.User).filter(
            models.User.email == newUser.email).first()
    if exists:
        raise HTTPException(status.HTTP_409_CONFLICT, "User with this email already exists in our system.")
    else:
        user_model = models.User(
            user_name=newUser.user_name,
            email=newUser.email,
            password_hash=passwordHash,
            salt=salt
        )
        db.add(user_model)
        db.commit()
    return user_model
