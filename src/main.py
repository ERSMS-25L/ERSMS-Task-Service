from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.database import get_session, engine
from src import models, schemas

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/ready")
async def ready():
    return {"status": "ready"}

@app.post("/task/create", response_model=schemas.TaskResponse)
async def create_task(task: schemas.TaskCreate, session: AsyncSession = Depends(get_session)):
    new_task = models.Task(
        title=task.title,
        description=task.description,
        user_email=task.user_email,
        status="pending"
    )
    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)
    return new_task

@app.get("/task/{task_id}", response_model=schemas.TaskResponse)
async def get_task(task_id: int, session: AsyncSession = Depends(get_session)):
    stmt = select(models.Task).where(models.Task.id == task_id)
    result = await session.execute(stmt)
    task = result.scalar_one_or_none()
    if task:
        return task
    return {"error": "Task not found"}

@app.get("/task/by-user/{email}", response_model=list[schemas.TaskResponse])
async def get_tasks_by_user(email: str, session: AsyncSession = Depends(get_session)):
    stmt = select(models.Task).where(models.Task.user_email == email)
    result = await session.execute(stmt)
    tasks = result.scalars().all()
    return tasks

