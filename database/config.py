from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    is_completed: bool = False


class TaskCreate(TaskBase):
    pass


class TaskResponse(TaskBase):
    id: int


    class Config:
        orm_mode = True