from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
import schema, crud
import schemas
from database import get_db
from auth import get_current_user

router = APIRouter()

@router.post("/courses", response_model=schemas.Course, tags=["Course"])
async def create_course(
    course: schemas.CourseCreate,
    current_user: schemas.user = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> schemas.Course:
    # Create a new course with the current user as the owner
    new_course = crud.create_course(db, course, current_user)
    return new_course

@router.get("/courses/{course_id}", response_model=schemas.Course, tags=["Course"])
async def get_course(
    course_id: int,
    current_user: schemas.user = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> schemas.Course:
    # Retrieve the course and check if the current user is the owner
    course = crud.get_course(db, course_id)
    if not course or course.owner != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this course")
    return course

@router.put("/courses/{course_id}", response_model=schemas.Course, tags=["Course"])
async def update_course(
    course_id: int,
    course: schemas.CourseUpdate,
    current_user: schemas.user = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> schemas.Course:
    # Retrieve the course and check if the current user is the owner
    existing_course = crud.get_course(db, course_id)
    if not existing_course or existing_course.owner != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this course")
    
    # Update the course with the provided details
    updated_course = crud.update_course(db, course_id, **course.dict(exclude_unset=True))
    return updated_course

@router.delete("/courses/{course_id}", tags=["Course"])
async def delete_course(
    course_id: int,
    current_user: schemas.user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Retrieve the course and check if the current user is the owner
    existing_course = crud.get_course(db, course_id)
    if not existing_course or existing_course.owner != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this course")
    
    # Delete the course
    crud.delete_course(db, course_id)
    return {"detail": "Course deleted"}

@router.get("/courses", response_model=List[schemas.Course], tags=["Course"])
async def get_user_courses(
    current_user: schemas.user = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> List[schemas.Course]:
    # Fetch all courses owned by the current user
    courses = crud.get_courses_by_owner(db, current_user.id)
    return courses
