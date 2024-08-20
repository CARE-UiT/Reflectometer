from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import schema, auth
from database import get_db
import schemas

router = APIRouter()

@router.post("/token", tags=["Auth"])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = auth.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")

@router.post("/auth/new", tags=["Auth"])
async def new_user(newUser: schemas.NewUser, db: Session = Depends(get_db)):
    return auth.create_new_user(newUser, db)

@router.get("/auth/current", tags=["Auth"])
async def get_current_user(
    current_user: Annotated[schemas.User, Depends(auth.get_current_user)]
):
    return current_user
