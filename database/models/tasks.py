from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Column, DateTime, func

from database.models.task_detail import Tasks_detail


class TaskBase(SQLModel):
    title: str
    company: str = Field(max_length=100, nullable=True)
    price: float
    date: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    stars: int = Field(default=0, nullable=True)
    price_per_unit: float = Field(default=0, nullable=True)
    did: int = Field(default=0, nullable=True)


class Tasks(TaskBase, table=True):
    id: Optional[int] = Field(primary_key=True)

    column_id: int = Field(foreign_key="columns.id")
    column: Optional["Columns"] = Relationship(back_populates="tasks", sa_relationship_kwargs={"lazy": 'selectin'})
    detail: Optional[Tasks_detail] = Relationship(back_populates="task", sa_relationship_kwargs={"lazy": 'selectin'})


class TaskRead(TaskBase):
    id: int
    column_id: int


class TaskCreate(TaskBase):
    pass
