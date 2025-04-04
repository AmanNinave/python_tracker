from typing import List
from pydantic import BaseModel
from .task_schema import TaskResponse


class User(BaseModel):
    name:str
    email:str
    password:str

class ShowUser(BaseModel):
    name:str
    email:str
    # tasks: List[TaskResponse] = []  # Uncomment this line if we want to include tasks in the response ( not needed for now )
    class Config():
        orm_mode = True


