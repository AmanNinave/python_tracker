# Library imports
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

# File imports
from .. import database
from ..schemas import task_log_schema
from ..controllers import task_log_controller
from ..models import models
from ..utils.oauth2 import get_current_user

router = APIRouter(
    prefix="/task-log",
    tags=["task-logs"]
)

get_db = database.get_db

@router.post("/", response_model=task_log_schema.TaskLogResponse, status_code=status.HTTP_201_CREATED)
def create(request: task_log_schema.TaskLogCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return task_log_controller.create(db, request, user.id)

@router.get("/duration/", response_model=list[task_log_schema.TaskLogResponse])
def get_logs_by_duration(
    start_date: datetime, 
    end_date: datetime = None,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    user: models.User = Depends(get_current_user)
):
    """
    Get task logs within a specific date range.
    - start_date: Required start date (format: YYYY-MM-DDTHH:MM:SS)
    - end_date: Optional end date (defaults to current time if not provided)
    """
    if end_date is None:
        end_date = datetime.now()
        
    logs = task_log_controller.get_by_duration(db, user.id, start_date, end_date, skip, limit)
    return logs

@router.get("/{id}", response_model=task_log_schema.TaskLogResponse)
def read(id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    log = task_log_controller.get(db, id, user.id)
    if not log:
        raise HTTPException(status_code=404, detail="Task Log not found")
    return log

@router.get("/", response_model=list[task_log_schema.TaskLogResponse])
def read(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return task_log_controller.get_all(db, skip, limit, user.id)



@router.put("/{id}", response_model=task_log_schema.TaskLogResponse)
def update(id: int, request: task_log_schema.TaskLogUpdate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    updated_log = task_log_controller.update(db, id, request, user.id)
    if not updated_log:
        raise HTTPException(status_code=404, detail="Task Log not found")
    return updated_log

@router.delete("/{id}" , status_code=204)
def delete(id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    response = task_log_controller.delete(db, id, user.id)
    if not response:
        raise HTTPException(status_code=404, detail="Task Log not found")
    return 