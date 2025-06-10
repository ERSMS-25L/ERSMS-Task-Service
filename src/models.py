from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from datetime import datetime
from enum import Enum
from src.database import Base


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    user_id = Column(String(128), nullable=False, index=True)  # Firebase UID
    status = Column(
        SQLEnum(TaskStatus), default=TaskStatus.PENDING, nullable=False, index=True
    )
    priority = Column(
        SQLEnum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False, index=True
    )
    due_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    completed_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}')>"
