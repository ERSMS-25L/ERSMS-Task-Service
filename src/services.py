from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, and_, or_
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from src.models import Task, TaskStatus
from src.schemas import TaskCreate, TaskUpdate, TaskQuery


class TaskService:
    @staticmethod
    async def create_task(session: AsyncSession, task_data: TaskCreate) -> Task:
        """Create a new task"""
        task = Task(
            title=task_data.title,
            description=task_data.description,
            user_id=task_data.user_id,
            priority=task_data.priority,
            due_date=task_data.due_date,
            status=TaskStatus.PENDING,
        )

        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task

    @staticmethod
    async def get_task_by_id(
        session: AsyncSession, task_id: int, user_id: Optional[str] = None
    ) -> Optional[Task]:
        """Get task by ID"""
        stmt = select(Task).where(Task.id == task_id)

        if user_id:
            stmt = stmt.where(Task.user_id == user_id)

        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def update_task(
        session: AsyncSession, task: Task, update_data: TaskUpdate
    ) -> Task:
        """Update a task"""
        update_dict = update_data.model_dump(exclude_unset=True)

        for field, value in update_dict.items():
            if hasattr(task, field):
                setattr(task, field, value)

        if update_data.status == TaskStatus.COMPLETED and task.completed_at is None:
            task.completed_at = datetime.now(timezone.utc) + timedelta(hours=2)
        elif update_data.status != TaskStatus.COMPLETED:
            task.completed_at = None

        await session.commit()
        await session.refresh(task)
        return task

    @staticmethod
    async def delete_task(session: AsyncSession, task: Task) -> bool:
        """Delete a task"""
        await session.delete(task)
        await session.commit()
        return True

    @staticmethod
    async def get_tasks(
        session: AsyncSession, query: TaskQuery, user_id: Optional[str] = None
    ) -> Tuple[List[Task], int]:
        """Get tasks with filtering and pagination"""
        stmt = select(Task)
        count_stmt = select(func.count(Task.id))

        filters = []

        if user_id:
            filters.append(Task.user_id == user_id)
        elif query.user_id:
            filters.append(Task.user_id == query.user_id)

        if query.status:
            filters.append(Task.status == query.status)

        if query.priority:
            filters.append(Task.priority == query.priority)

        if query.search:
            search_filter = or_(
                Task.title.ilike(f"%{query.search}%"),
                Task.description.ilike(f"%{query.search}%"),
            )
            filters.append(search_filter)

        if filters:
            stmt = stmt.where(and_(*filters))
            count_stmt = count_stmt.where(and_(*filters))

        count_result = await session.execute(count_stmt)
        total = count_result.scalar()

        stmt = stmt.order_by(Task.created_at.desc())
        stmt = stmt.offset((query.page - 1) * query.size).limit(query.size)

        result = await session.execute(stmt)
        tasks = result.scalars().all()

        return tasks, total

    @staticmethod
    async def get_user_task_stats(session: AsyncSession, user_id: str) -> dict:
        """Get task statistics for a user"""
        stmt = (
            select(Task.status, func.count(Task.id).label("count"))
            .where(Task.user_id == user_id)
            .group_by(Task.status)
        )

        result = await session.execute(stmt)
        stats = {status.value: 0 for status in TaskStatus}

        for row in result:
            stats[row.status] = row.count

        return stats
