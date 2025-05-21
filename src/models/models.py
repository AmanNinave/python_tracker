# Library imports
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

# File imports
from ..database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))
    # avatar = Column(String(255), nullable=True)  # Avatar URL or path
    # settings = Column(JSON, nullable=True)  # Storing list as JSON ( color, icon, type)
    # privileges = Column(JSON, nullable=True)  # Storing list as JSON ( color, icon, type)

    tasks = relationship("Task", back_populates="user") # Relationship with Task

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    category = Column(String(255), nullable=False)   # Category of task (e.g., work, routine, personal)
    sub_category = Column(String(255), nullable=False)    # Sub-category of task (e.g., sleep, frontend, backend)

    title = Column(String(255), nullable=True)  # Title of task
    description = Column(String(1000), nullable=True)    # Description of task ( Intigrate with markdown later)

    status = Column(String(255), default='pending') # status :- pending : task yet to start, inprogress : routines, completed : short tasks, scheduled : future task tasks
    
    indicators = Column(JSON, nullable=True)  # Storing list as JSON ( remarks,rating, priority)
    settings = Column(JSON, nullable=True)  # Storing list as JSON ( color, icon, type)
        
    user_id = Column(Integer, ForeignKey("users.id"))  # Foreign key to User

    user = relationship("User", back_populates="tasks")  # Relationship with User
    task_schedules = relationship("TaskSchedule", back_populates="task")  # Relationship with TaskSchedule

class TaskSchedule(Base):
    __tablename__ = "task_schedule"

    id = Column(Integer, primary_key=True, index=True)  # Unique identifier for the schedule entry

    start_time = Column(DateTime, nullable=False)   # Start time of the schedule entry
    end_time = Column(DateTime, nullable=False)  # End time of the schedule entry
    remarks = Column(String(1000), nullable=True)  # Remarks for the schedule entry

    user_id = Column(Integer, ForeignKey("users.id"))  # Foreign key to User
    task_id = Column(Integer, ForeignKey("tasks.id"))  # Foreign key to Tasks

    task = relationship("Task", back_populates="task_schedules")  # Relationship with Task
    task_logs = relationship("TaskLog", back_populates="task_schedule")  # Relationship with TaskLog


class TaskLog(Base):
    __tablename__ = "task_log"

    id = Column(Integer, primary_key=True, index=True)  # Unique identifier for the log entry

    start_time = Column(DateTime, nullable=True)   # Start time of the log entry
    end_time = Column(DateTime, nullable=True)  # End time of the log entry
    remarks = Column(String(1000), nullable=True)  # Remarks for the log entry

    user_id = Column(Integer, ForeignKey("users.id"))  # Foreign key to User
    task_id = Column(Integer, ForeignKey("tasks.id"))  # Foreign key to Tasks
    task_schedule_id = Column(Integer, ForeignKey("task_schedule.id"))  # Foreign key to TaskSchedule

    task = relationship("Task")  # Relationship with Task
    task_schedule = relationship("TaskSchedule", back_populates="task_logs")  # Relationship with TaskSchedule


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)  # Unique identifier for the event entry

    start_time = Column(DateTime, nullable=True)   # Start time of the event entry
    end_time = Column(DateTime, nullable=True)  # End time of the event entry

    category = Column(String(255), nullable=True)  # Category of event (e.g., work, routine, personal)
    sub_category = Column(String(255), nullable=True)  # Sub-category of event (e.g., sleep, frontend, backend)

    title = Column(String(255), nullable=True)  # Title of event
    description = Column(String(1000), nullable=True)  # Description of event ( Intigrate with markdown later)

    indicators = Column(JSON, nullable=True)  # Storing list as JSON ( remarks,rating, priority)
    settings = Column(JSON, nullable=True)  # Storing list as JSON ( color, icon, type)

    user_id = Column(Integer, ForeignKey("users.id"))  # Foreign key to User