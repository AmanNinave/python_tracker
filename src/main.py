# Library imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# File imports
from .database import engine
from .models import models
from .routes import user_route, authentication_route, task_route, task_schedule_route, task_log_route

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust based on your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Comment this out for Vercel deployment
models.Base.metadata.create_all(engine)

app.include_router(authentication_route.router)
app.include_router(user_route.router)
app.include_router(task_route.router)
app.include_router(task_schedule_route.router)
app.include_router(task_log_route.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Task Management API"}

