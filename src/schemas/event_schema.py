from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime


class EventBase(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    category: Optional[str] = None
    sub_category: Optional[str] = None

    title: Optional[str] = None
    description: Optional[str] = None

    indicators: Optional[Any] = {}  # Dictionary to store remarks, rating, status, priority
    settings: Optional[Any] = {}  
    

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    id: int      # Task associated with this schedule
    class Config:
        from_attributes = True

