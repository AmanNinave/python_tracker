# Library imports
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

# File imports
from ..database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    # avatar = Column(String, nullable=True)  # Avatar URL or path
    # settings = Column(JSON, nullable=True)  # Storing list as JSON ( color, icon, type)
    # privileges = Column(JSON, nullable=True)  # Storing list as JSON ( color, icon, type)

    tasks = relationship("Task", back_populates="user") # Relationship with Task

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    category = Column(String, nullable=False)   # Category of task (e.g., work, routine, personal)
    sub_category = Column(String, nullable=False)    # Sub-category of task (e.g., sleep, frontend, backend)

    title = Column(String, nullable=True)  # Title of task
    description = Column(String, nullable=True)    # Description of task ( Intigrate with markdown later)

    planned_time = Column(DateTime, nullable=True)   # Planned start time of task (Optional :- will show as unplanned)
    duration = Column(Integer, nullable=True)  # duration of task in minutes

    indicators = Column(JSON, nullable=True)  # Storing list as JSON ( remarks,rating, status, priority)
    settings = Column(JSON, nullable=True)  # Storing list as JSON ( color, icon, type)
        
    user_id = Column(Integer, ForeignKey("users.id"))  # Foreign key to User

    user = relationship("User", back_populates="tasks")  # Relationship with User
    task_logs = relationship("TaskLog", back_populates="task")  # Relationship with TaskLog


class TaskLog(Base):
    __tablename__ = "task_log"

    id = Column(Integer, primary_key=True, index=True)  # Unique identifier for the log entry

    start_time = Column(DateTime, nullable=False)   # Start time of the log entry
    end_time = Column(DateTime, nullable=True)  # End time of the log entry

    task_id = Column(Integer, ForeignKey("tasks.id"))  # Foreign key to Tasks
    # user_id = Column(Integer, ForeignKey("users.id"))  # Foreign key to User ( not needed as task_id is already linked to user)

    task = relationship("Task", back_populates="task_logs")  # Relationship with Event
