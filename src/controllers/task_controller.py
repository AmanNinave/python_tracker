# Library imports
from sqlalchemy.orm import Session
from sqlalchemy import update
from fastapi import HTTPException,status

# File imports
from ..schemas import task_schema
from ..models import models

def create(request: task_schema.TaskCreate, db: Session , user_id: int):
    if not request.category or not request.sub_category:
        raise HTTPException(status_code=400, detail="Required fields are missing")

    new_task = models.Task(
        category=request.category,
        sub_category=request.sub_category,

        title=request.title,
        description=request.description,

        status=request.status,

        indicators=request.indicators,
        settings=request.settings,

        user_id=user_id 
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"success": True}

def get_all(db: Session , user_id: int):
    return db.query(models.Task).filter(models.Task.user_id == user_id).all()

def get(id: int, db: Session, user_id: int):
    task = db.query(models.Task).filter((models.Task.user_id == user_id) & (models.Task.id == id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

def delete(id: int, db: Session, user_id: int):
    task = db.query(models.Task).filter((models.Task.user_id == user_id) & (models.Task.id == id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"success": True}

def update_task(id: int, updates: task_schema.TaskUpdate, db: Session, user_id: int):
    # Check if the task exists
    task = db.query(models.Task).filter((models.Task.user_id == user_id) & (models.Task.id == id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Convert updates to a dictionary, ignoring unset fields
    update_data = updates.model_dump(exclude_unset=True)

    if not update_data:  # Prevent empty updates
        raise HTTPException(status_code=400, detail="No valid fields to update")

    # Perform the update using SQLAlchemy
    db.execute(
        update(models.Task)
        .where(models.Task.id == id)
        .values(**update_data)
    )

    db.commit()

    return {"success": True, "message": "Task updated successfully"}
