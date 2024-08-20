from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date as datetype

class CourseBase(BaseModel):
    name: str = Field(..., example="Course Name")
    password_hash: Optional[str] = Field(None, example="hashedpassword")
    salt: Optional[str] = Field(None, example="randomsalt")
    date: datetype = Field(..., example="2024-08-13")
    description: Optional[str] = Field(None, example="This is a description of the course.")

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    name: Optional[str] = Field(None, example="New Course Name")
    password_hash: Optional[str] = Field(None, example="newhashedpassword")
    salt: Optional[str] = Field(None, example="newsalt")

class Course(CourseBase):
    id: int
    owner: int

    class Config:
        orm_mode = True
