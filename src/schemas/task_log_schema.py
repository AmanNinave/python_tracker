from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from .task_schema import Task


class TaskLogBase(BaseModel):
    start_time: datetime
    end_time: Optional[datetime] = None
    task_id: int

class TaskLogCreate(TaskLogBase):
    pass

class TaskLogUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class TaskLogResponse(TaskLogBase):
    id: int
    # task: Task  ( Not needed as it will be fetched from task_id)

    class Config:
        orm_mode = True
        from_attributes = True

class SuccessResponse(BaseModel):
    success: bool

    class Config:
        orm_mode = True
