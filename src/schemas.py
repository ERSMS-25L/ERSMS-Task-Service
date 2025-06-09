from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str
    user_email: str  # 👈 importante para asociar la tarea al usuario

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    user_email: str
    status: str

    class Config:
        orm_mode = True

