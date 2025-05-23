# Library imports
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

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
    return task_schedule_controller.create(db, request, user.id)

@router.get("/duration/", response_model=list[task_schedule_schema.TaskScheduleResponse])
def get_schedules_by_duration(
    start_date: datetime, 
    end_date: datetime = None,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    user: models.User = Depends(get_current_user)
):
    """
    Get task schedules within a specific date range.
    - start_date: Required start date (format: YYYY-MM-DDTHH:MM:SS)
    - end_date: Optional end date (defaults to current time if not provided)
    """
    if end_date is None:
        end_date = datetime.now()
        
    schedules = task_schedule_controller.get_by_duration(db, user.id, start_date, end_date, skip, limit)
    return schedules

@router.get("/{id}", response_model=task_schedule_schema.TaskScheduleResponse)
def read(id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    schedule = task_schedule_controller.get(db, id, user.id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Task schedule not found")
    return schedule

@router.get("/", response_model=list[task_schedule_schema.TaskScheduleResponse])
def read(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return task_schedule_controller.get_all(db, skip, limit, user.id)

@router.put("/{id}", response_model=task_schedule_schema.TaskScheduleResponse)
def update(id: int, request: task_schedule_schema.TaskScheduleUpdate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    updated_schedule = task_schedule_controller.update(db, id, request, user.id)
    if not updated_schedule:
        raise HTTPException(status_code=404, detail="Task schedule not found")
    return updated_schedule

@router.delete("/{id}" , status_code=204)
def delete(id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    response = task_schedule_controller.delete(db, id, user.id)
    if not response:
        raise HTTPException(status_code=404, detail="Task schedule not found")
    return 