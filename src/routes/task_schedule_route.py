# Library imports
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# File imports
from .. import database
from ..schemas import task_schedule_schema
from ..controllers import task_schedule_controller
from ..models import models
from ..utils.oauth2 import get_current_user

router = APIRouter(
    prefix="/task-schedule",
    tags=["task-schedules"]
)

get_db = database.get_db

@router.post("/", response_model=task_schedule_schema.TaskScheduleResponse, status_code=status.HTTP_201_CREATED)
def create(request: task_schedule_schema.TaskScheduleCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return task_schedule_controller.create(db, request)

@router.get("/{id}", response_model=task_schedule_schema.TaskScheduleResponse)
def read(id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    schedule = task_schedule_controller.get(db, id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Task schedule not found")
    return schedule

@router.get("/", response_model=list[task_schedule_schema.TaskScheduleResponse])
def read(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return task_schedule_controller.get_all(db, skip, limit)

@router.put("/{id}", response_model=task_schedule_schema.TaskScheduleResponse)
def update(id: int, request: task_schedule_schema.TaskScheduleUpdate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    updated_schedule = task_schedule_controller.update(db, id, request)
    if not updated_schedule:
        raise HTTPException(status_code=404, detail="Task schedule not found")
    return updated_schedule

@router.delete("/{id}" , status_code=204)
def delete(id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    response = task_schedule_controller.delete(db, id)
    if not response:
        raise HTTPException(status_code=404, detail="Task schedule not found")
    return 