from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from .task_log_schema import TaskLogResponse
from .task_schema import Task

class TaskScheduleBase(BaseModel):
    start_time: datetime
    end_time: Optional[datetime] = None
    remarks: Optional[str] = None

    task_id: int

class TaskScheduleCreate(TaskScheduleBase):
    pass

class TaskScheduleUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    remarks: Optional[str] = None


class TaskScheduleResponse(TaskScheduleBase):
    id: int
    task : Task   # Task associated with this schedule
    task_logs: List[TaskLogResponse] = []  # List of task logs associated with this schedule
    
    class Config:
        from_attributes = True

