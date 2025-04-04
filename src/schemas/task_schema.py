# Library imports
from typing import List, Optional, Dict
from pydantic import BaseModel
from datetime import datetime

# File imports

class TaskLogBase(BaseModel):
    start_time: datetime
    end_time: Optional[datetime] = None
    id: int

# Base Task Schema (Common fields for Task)
class TaskBase(BaseModel):

    category: str           # Category of task (e.g., work, routine, personal)
    sub_category: str       # Sub-category of task (e.g., sleep, frontend, backend)

    title: Optional[str] = None
    description: Optional[str] = None

    planned_time: Optional[datetime] = None  # Planned start time of task (Optional :- will show as unplanned)
    duration: Optional[int] = None  # Duration of task in minutes

    indicators: Optional[Dict[str, str]] = {}  # Dictionary to store remarks, rating, status, priority
    settings: Optional[Dict[str, str]] = {}  # Dictionary to store color, icon, type


class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True


# Schema for Creating an Task (Extends TaskBase)
class TaskCreate(TaskBase):
    pass
    class Config():
            orm_mode = True

# Schema for Updating an Task (Allows Partial Updates)
class TaskUpdate(BaseModel):
    category: Optional[str] = None           # Category of task (e.g., work, routine, personal)
    sub_category: Optional[str] = None       # Sub-category of task (e.g., sleep, frontend, backend)

    title: Optional[str] = None
    description: Optional[str] = None

    planned_time: Optional[datetime] = None  # Planned start time of task (Optional :- will show as unplanned)
    duration: Optional[int] = None  # Duration of task in minutes

    indicators: Optional[Dict[str, str]] = {}  # Dictionary to store remarks, rating, status, priority
    settings: Optional[Dict[str, str]] = {}  # Dictionary to store color, icon, type


# Schema for Returning Task Details
class TaskResponse(TaskBase):
    id: int
    user_id:int
    task_logs: List[TaskLogBase] = []  # List of TaskLogResponse objects

    class Config:
        orm_mode = True  # Allows compatibility with SQLAlchemy ORM


