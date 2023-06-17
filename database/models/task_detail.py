from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship, Column, DateTime, func


class TaskDetailBase(SQLModel):
    title: str = Field(max_length=100, nullable=True)


class Tasks_detail(TaskDetailBase, table=True):
    id: Optional[int] = Field(primary_key=True)

    task_id: int = Field(foreign_key="tasks.id")
    task: Optional['Tasks'] = Relationship(back_populates="detail", sa_relationship_kwargs={"lazy": 'selectin'})


class TaskDetailRead(TaskDetailBase):
    id: int
    pass


class TaskDetailCreate(TaskDetailBase):
    pass
