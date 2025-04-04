# Library imports
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# File imports
from .. import database
from ..schemas import task_log_schema
from ..controllers import task_log_controller

router = APIRouter(
    prefix="/task-log",
    tags=["task-logs"]
)

get_db = database.get_db

@router.post("/", response_model=task_log_schema.TaskLogResponse, status_code=status.HTTP_201_CREATED)
def create(request: task_log_schema.TaskLogCreate, db: Session = Depends(get_db)):
    return task_log_controller.create(db, request)

@router.get("/{id}", response_model=task_log_schema.TaskLogResponse)
def read(id: int, db: Session = Depends(get_db)):
    log = task_log_controller.get(db, id)
    if not log:
        raise HTTPException(status_code=404, detail="Task Log not found")
    return log

@router.get("/", response_model=list[task_log_schema.TaskLogResponse])
def read(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return task_log_controller.get_all(db, skip, limit)

@router.put("/{id}", response_model=task_log_schema.TaskLogResponse)
def update(id: int, request: task_log_schema.TaskLogUpdate, db: Session = Depends(get_db)):
    updated_log = task_log_controller.update(db, id, request)
    if not updated_log:
        raise HTTPException(status_code=404, detail="Task Log not found")
    return updated_log

@router.delete("/{id}" , status_code=204)
def delete(id: int, db: Session = Depends(get_db)):
    response = task_log_controller.delete(db, id)
    if not response:
        raise HTTPException(status_code=404, detail="Task Log not found")
    return 