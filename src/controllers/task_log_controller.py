# Library imports
from sqlalchemy.orm import Session
from sqlalchemy import update
from fastapi import HTTPException,status
from datetime import datetime

# File imports
from ..schemas import task_log_schema
from ..models import models
# from .. import models, schemas

def create(db: Session, request: task_log_schema.TaskLogCreate, user_id: int):
    new_log = models.TaskLog(
        start_time=request.start_time,
        end_time=request.end_time,
        task_schedule_id=request.task_schedule_id,
        task_id=request.task_id,
        remarks=request.remarks,

        user_id=user_id,
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

def get_by_duration(db: Session, user_id: int, start_date: datetime, end_date: datetime, skip: int = 0, limit: int = 100):
    """Get task logs within a specific date range."""
    return db.query(models.TaskLog)\
        .filter(
            models.TaskLog.user_id == user_id,
            models.TaskLog.start_time >= start_date,
            models.TaskLog.start_time <= end_date
        )\
        .order_by(models.TaskLog.start_time.asc())\
        .offset(skip)\
        .limit(limit)\
        .all()

def get(db: Session, log_id: int, user_id: int):
    return db.query(models.TaskLog).filter(models.TaskLog.user_id == user_id).filter(models.TaskLog.id == log_id).first()

def get_all(db: Session, skip: int = 0, limit: int = 10, user_id: int = None):
    return db.query(models.TaskLog).filter(models.TaskLog.user_id == user_id).offset(skip).limit(limit).all()

def update(db: Session, log_id: int, log_update: task_log_schema.TaskLogUpdate, user_id: int):
    db_log = db.query(models.TaskLog).filter(models.TaskLog.user_id == user_id).filter(models.TaskLog.id == log_id).first()
    if db_log is None:
        return None
    for key, value in log_update.dict(exclude_unset=True).items():
        setattr(db_log, key, value)
    db.commit()
    db.refresh(db_log)
    return db_log

def delete(db: Session, id: int, user_id: int):
    db_log = db.query(models.TaskLog).filter(models.TaskLog.user_id == user_id).filter(models.TaskLog.id == id).first()
    if db_log:
        db.delete(db_log)
        db.commit()
        return True
    return False

