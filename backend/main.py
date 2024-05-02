import os
from fastapi import FastAPI, HTTPException, Depends, status, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from database import engine, get_db, Base
from sqlalchemy.orm import Session
import models, schema
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
import auth
from datetime import timedelta
FILE_STORAGE_PATH = "/files/"

app = FastAPI()

origins = [
    'http://localhost:5173',
    'http://localhost:4173',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

@app.post("/api/token", tags=["Auth"])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db: Session = Depends(get_db)):
    user = auth.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.user_name}, expires_delta=access_token_expires
    )
    return schema.Token(access_token=access_token, token_type="bearer")

@app.post("/api/auth/new", tags=["Auth"])
async def new_user(newPilot : schema.User, db: Session = Depends(get_db)):
    return auth.create_new_user(newPilot,db)

@app.get("/api/auth/current", tags=["Auth"])
async def get_current_user(
    current_user: Annotated[schema.User, Depends(auth.get_current_user)]
):
    return current_user
