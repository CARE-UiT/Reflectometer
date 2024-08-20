from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import schema, crud
from database import get_db

router = APIRouter()

@router.post("/participant", tags=["Participant"])
async def create_participant(
    participant: schema.Participant,
    db: Session = Depends(get_db)
) -> schema.Participant | None:
    return crud.create_participant(participant, db)

@router.get("/participant", tags=["Participant"])
async def get_participant(
    id: int,
    db: Session = Depends(get_db),
) -> schema.Participant:
    res = crud.get_participant(id, db)
    if res == None:
        raise HTTPException(404, detail="Participant not found")
    return res

@router.delete("/participant", tags=["Participant"])
async def delete_participant(
    id: Annotated[int, "ID of participant"],
    db: Session = Depends(get_db),
):
    crud.delete_participant(id, db)
