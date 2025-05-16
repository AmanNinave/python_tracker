# Library imports
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

# File imports

class TaskSchduleAndLogBase(BaseModel):
    id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    remarks: Optional[str] = None
class TaskLogResponse(TaskSchduleAndLogBase):
    pass

class TaskScheduleResponse(TaskSchduleAndLogBase):
    task_logs: List[TaskLogResponse] = []  # List of task logs associated with this schedule


# Base Task Schema (Common fields for Task)
class TaskBase(BaseModel):

    category: str           # Category of task (e.g., work, routine, personal)
    sub_category: str       # Sub-category of task (e.g., sleep, frontend, backend)

    title: Optional[str] = None
    description: Optional[str] = None

    status: str = 'pending'

    indicators: Optional[Dict[str, str]] = {}  # Dictionary to store remarks, rating, status, priority
    settings: Optional[Dict[str, str]] = {}  # Dictionary to store color, icon, type


class Task(TaskBase):
    id: int

    class Config:
        from_attributes = True


# Schema for Creating an Task (Extends TaskBase)
class TaskCreate(TaskBase):
    pass
    class Config():
            from_attributes = True

# Schema for Updating an Task (Allows Partial Updates)
class TaskUpdate(BaseModel):
    category: Optional[str] = None           # Category of task (e.g., work, routine, personal)
    sub_category: Optional[str] = None       # Sub-category of task (e.g., sleep, frontend, backend)

    title: Optional[str] = None
    description: Optional[str] = None

    status: str = 'pending'

    indicators: Optional[Any] = {}  # Dictionary to store remarks, rating, status, priority
    settings: Optional[Any] = {}  # Dictionary to store color, icon, type


# Schema for Returning Task Details
class TaskResponse(TaskBase):
    id: int
    user_id:int
    task_schedules: List[TaskScheduleResponse] = []  # List of TaskSchedulesResponse objects

    class Config:
        from_attributes = True  # Allows compatibility with SQLAlchemy ORM


