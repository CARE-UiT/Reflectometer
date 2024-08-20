import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models
from endpoints import auth, course, participant, session, curve, keymoment

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

# Include the routers
app.include_router(auth.router, prefix="/api")
app.include_router(session.router, prefix="/api")
app.include_router(participant.router, prefix="/api")
app.include_router(course.router, prefix="/api")
app.include_router(curve.router, prefix="/api")
app.include_router(keymoment.router, prefix="/api")


