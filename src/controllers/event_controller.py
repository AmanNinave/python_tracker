from sqlalchemy.orm import Session
from datetime import datetime

# File imports
from ..schemas import event_schema
from ..models import models

def create(db: Session, request: event_schema.EventCreate, user_id: int):
    """Create a new event"""
    new_event = models.Event(
        start_time=request.start_time,
        end_time=request.end_time,
        category=request.category,
        sub_category=request.sub_category,
        title=request.title,
        description=request.description,
        indicators=request.indicators,
        settings=request.settings,
        user_id=user_id
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

def get(db: Session, event_id: int, user_id: int):
    """Get a specific event by ID"""
    return db.query(models.Event).filter(
        models.Event.id == event_id,
        models.Event.user_id == user_id
    ).first()

def get_all(db: Session, skip: int = 0, limit: int = 100, user_id: int = None):
    """Get all events for a user"""
    return db.query(models.Event).filter(
        models.Event.user_id == user_id
    ).offset(skip).limit(limit).all()

def get_by_duration(db: Session, user_id: int, start_date: datetime, end_date: datetime, skip: int = 0, limit: int = 100):
    """Get events within a specific date range"""
    return db.query(models.Event).filter(
        models.Event.user_id == user_id,
        # Events that start within the range
        ((models.Event.start_time >= start_date) & (models.Event.start_time <= end_date)) |
        # Events that end within the range
        ((models.Event.end_time >= start_date) & (models.Event.end_time <= end_date)) |
        # Events that span across the range
        ((models.Event.start_time <= start_date) & (models.Event.end_time >= end_date))
    ).order_by(models.Event.start_time.asc()).offset(skip).limit(limit).all()

def update(db: Session, event_id: int, event_data: event_schema.EventCreate, user_id: int):
    """Update an existing event"""
    db_event = db.query(models.Event).filter(
        models.Event.id == event_id,
        models.Event.user_id == user_id
    ).first()
    
    if db_event:
        # Update all fields
        for key, value in event_data.dict().items():
            setattr(db_event, key, value)
        
        db.commit()
        db.refresh(db_event)
    
    return db_event

def delete(db: Session, event_id: int, user_id: int):
    """Delete an event"""
    db_event = db.query(models.Event).filter(
        models.Event.id == event_id,
        models.Event.user_id == user_id
    ).first()
    
    if db_event:
        db.delete(db_event)
        db.commit()
        return True
    
    return False