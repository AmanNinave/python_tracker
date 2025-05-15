# Library imports
from sqlalchemy.orm import Session
from sqlalchemy import update
from fastapi import HTTPException,status

# File imports
from ..schemas import task_schedule_schema
from ..models import models
# from .. import models, schemas

def create(db: Session, request: task_schedule_schema.TaskScheduleCreate, user_id: int):
    new_schedule = models.TaskSchedule(
        start_time=request.start_time,
        end_time=request.end_time,
        remarks=request.remarks,
        
        task_id=request.task_id,
        user_id=user_id 
    )
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    return new_schedule

def get(db: Session, schedule_id: int, user_id: int):
    return db.query(models.TaskSchedule).filter(models.TaskSchedule.user_id == user_id).filter(models.TaskSchedule.id == schedule_id).first()

def get_all(db: Session, skip: int = 0, limit: int = 10, user_id: int = None):
    return db.query(models.TaskSchedule).filter(models.TaskSchedule.user_id == user_id).offset(skip).limit(limit).all()

def update(db: Session, schedule_id: int, schedule_update: task_schedule_schema.TaskScheduleUpdate, user_id: int):
    db_schedule = db.query(models.TaskSchedule).filter(models.TaskSchedule.user_id == user_id).filter(models.TaskSchedule.id == schedule_id).first()
    if db_schedule is None:
        return None
    for key, value in schedule_update.dict(exclude_unset=True).items():
        setattr(db_schedule, key, value)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

def delete(db: Session, id: int, user_id: int):
    db_schedule = db.query(models.TaskSchedule).filter(models.TaskSchedule.user_id == user_id).filter(models.TaskSchedule.id == id).first()
    if db_schedule:
        db.delete(db_schedule)
        db.commit()
        return True
    return False

