from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Fake in-memory database
tasks_db = []

# Task schema
class Task(BaseModel):
    title: str
    description: str

# Health checks
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/ready")
def readiness_check():
    return {"status": "ready"}

# Create a task
@app.post("/tasks")
def create_task(task: Task):
    tasks_db.append(task)
    return task

# List all tasks
@app.get("/tasks", response_model=List[Task])
def list_tasks():
    return tasks_db
