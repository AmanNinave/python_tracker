from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from .task_schema import Task


class TaskLogBase(BaseModel):
    start_time: datetime
    end_time: Optional[datetime] = None
    remarks: Optional[str] = None
    task_schedule_id: int
    task_id: Optional[int] = None

class TaskLogCreate(TaskLogBase):
    pass

class TaskLogUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    remarks: Optional[str] = None


class TaskLogResponse(TaskLogBase):
    id: int

    class Config:
        from_attributes = True

