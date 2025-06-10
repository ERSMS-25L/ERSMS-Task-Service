from pydantic import BaseModel, field_validator, Field
from typing import Optional, List
from datetime import datetime
from src.models import TaskStatus, TaskPriority


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None

    @field_validator("title")
    def validate_title(cls, v):
        if not v or not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()


class TaskCreateRequest(TaskBase):
    pass


class TaskCreate(TaskBase):
    user_id: str  # Firebase UID


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None

    @field_validator("title")
    def validate_title(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError("Title cannot be empty")
        return v.strip() if v else None


class TaskResponse(TaskBase):
    id: int
    user_id: str  # Firebase UID
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]
    total: int
    page: int
    size: int
    total_pages: int


class TaskQuery(BaseModel):
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    user_id: Optional[str] = None  # Firebase UID for admin queries
    search: Optional[str] = Field(None, max_length=255)
    page: int = Field(1, ge=1)
    size: int = Field(20, ge=1, le=100)


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    service: str
    version: str


class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime
