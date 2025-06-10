from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone
from typing import List, Optional
import math

from src.config import settings
from src.database import get_session, create_tables
from src.models import Task
from src.schemas import (
    TaskCreate,
    TaskCreateRequest,
    TaskUpdate,
    TaskResponse,
    TaskListResponse,
    TaskQuery,
    HealthResponse,
    ErrorResponse,
)
from src.services import TaskService
from src.auth import get_current_user, FirebaseUser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(
    title=settings.SERVICE_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    return HealthResponse(
        status="ok",
        timestamp=datetime.now(timezone.utc) + timedelta(hours=2),
        service=settings.SERVICE_NAME,
        version=settings.VERSION,
    )


@app.get("/ready", response_model=HealthResponse)
async def ready():
    """Readiness check endpoint"""
    return HealthResponse(
        status="ready",
        timestamp=datetime.now(timezone.utc) + timedelta(hours=2),
        service=settings.SERVICE_NAME,
        version=settings.VERSION,
    )


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreateRequest,
    current_user: FirebaseUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Create a new task"""
    task_create = TaskCreate(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        due_date=task_data.due_date,
        user_id=current_user.uid,
    )
    task = await TaskService.create_task(session, task_create)
    return task


@app.get("/tasks", response_model=TaskListResponse)
async def list_tasks(
    status_filter: Optional[str] = Query(None, alias="status"),
    priority: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    current_user: FirebaseUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """List tasks for the current user with filtering and pagination"""
    query = TaskQuery(
        status=status_filter, priority=priority, search=search, page=page, size=size
    )

    tasks, total = await TaskService.get_tasks(session, query, current_user.uid)
    total_pages = math.ceil(total / size) if total > 0 else 0

    return TaskListResponse(
        tasks=tasks, total=total, page=page, size=size, total_pages=total_pages
    )


@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user: FirebaseUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Get a specific task by ID"""
    task = await TaskService.get_task_by_id(session, task_id, current_user.uid)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    return task


@app.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: FirebaseUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Update a specific task"""
    task = await TaskService.get_task_by_id(session, task_id, current_user.uid)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    updated_task = await TaskService.update_task(session, task, task_update)
    return updated_task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user: FirebaseUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Delete a specific task"""
    task = await TaskService.get_task_by_id(session, task_id, current_user.uid)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    await TaskService.delete_task(session, task)


@app.get("/users/me/stats")
async def get_user_stats(
    current_user: FirebaseUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Get current user's task statistics"""
    stats = await TaskService.get_user_task_stats(session, current_user.uid)
    return {
        "user_id": current_user.uid,
        "user_email": current_user.email,
        "task_stats": stats,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app", host="0.0.0.0", port=settings.SERVICE_PORT, reload=settings.DEBUG
    )
