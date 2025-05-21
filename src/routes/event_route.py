from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

# File imports
from ..controllers import event_controller
from ..database import get_db
from ..models import models
from ..schemas import event_schema
from ..utils.oauth2 import get_current_user

router = APIRouter(
    prefix="/event",
    tags=["Events"]
)

@router.post("/", response_model=event_schema.EventResponse, status_code=status.HTTP_201_CREATED)
def create(request: event_schema.EventCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    """
    Create a new event
    """
    return event_controller.create(db, request, user.id)

@router.get("/", response_model=List[event_schema.EventResponse])
def get_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    """
    Get all events for the current user
    """
    return event_controller.get_all(db, skip, limit, user.id)

@router.get("/duration/", response_model=List[event_schema.EventResponse])
def get_events_by_duration(
    start_date: datetime, 
    end_date: datetime = None,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    user: models.User = Depends(get_current_user)
):
    """
    Get events within a specific date range.
    - start_date: Required start date (format: YYYY-MM-DDTHH:MM:SS)
    - end_date: Optional end date (defaults to current time if not provided)
    """
    if end_date is None:
        end_date = datetime.now()
        
    events = event_controller.get_by_duration(db, user.id, start_date, end_date, skip, limit)
    return events

@router.get("/{id}", response_model=event_schema.EventResponse)
def read(id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    """
    Get a specific event by ID
    """
    event = event_controller.get(db, id, user.id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event with ID {id} not found")
    return event

@router.put("/{id}", response_model=event_schema.EventResponse)
def update(id: int, request: event_schema.EventCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    """
    Update an existing event
    """
    updated_event = event_controller.update(db, id, request, user.id)
    if not updated_event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event with ID {id} not found")
    return updated_event

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    """
    Delete an event
    """
    if not event_controller.delete(db, id, user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event with ID {id} not found")