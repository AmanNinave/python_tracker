# Library imports
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# File imports
from .. import database
from ..controllers import task_controller
from ..schemas import task_schema 

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

get_db = database.get_db

@router.post("/", status_code=status.HTTP_201_CREATED,)
def create(request: task_schema.TaskCreate, db: Session = Depends(get_db)):
    return task_controller.create(request, db)

@router.get("/", response_model=List[task_schema.TaskResponse])
def get_all(db: Session = Depends(get_db)):
    return task_controller.get_all(db)

# Get a specific task by ID
@router.get("/{id}", response_model=task_schema.TaskResponse)
def get(id: int, db: Session = Depends(get_db)):
    return task_controller.get(id, db)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    return task_controller.delete(id, db)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, updates: task_schema.TaskUpdate, db: Session = Depends(get_db)):
    return task_controller.update_task(id, updates, db)


