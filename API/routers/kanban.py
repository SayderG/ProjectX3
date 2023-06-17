from typing import List

from database.repositories.kanbanRepository import KanbanRepository
from fastapi import APIRouter, Depends, HTTPException
from database.base import AsyncDatabase
from database.models.funnels import FunnelRead, FunnelCreate, FunnelReadAll
from database.models.columns import ColumnRead, ColumnCreate, ColumnReadWithCount
from database.models.tasks import TaskRead, TaskCreate

router = APIRouter()


@router.post("/", response_model=FunnelRead, status_code=201)
async def create_funnel(funnel: FunnelCreate, db=Depends(AsyncDatabase.get_session)):
    return await KanbanRepository(db).create(funnel)


@router.get("/", response_model=list[FunnelReadAll])
async def get_funnels(db=Depends(AsyncDatabase.get_session)):
    return await KanbanRepository(db).all()


@router.get("/{funnel_id}", response_model=FunnelReadAll)
async def get_funnel(funnel_id: int, db=Depends(AsyncDatabase.get_session)):
    funnel = await KanbanRepository(db).get(funnel_id)
    if not funnel:
        raise HTTPException(status_code=404, detail="Funnel not found")
    return funnel


# columns
@router.post("/{funnel_id}/columns", response_model=ColumnRead, status_code=201)
async def create_column(funnel_id: int, column: ColumnCreate, db=Depends(AsyncDatabase.get_session)):
    funnel = await KanbanRepository(db).get(funnel_id)
    if not funnel:
        raise HTTPException(status_code=404, detail="Funnel not found")
    return await KanbanRepository(db).create_column(funnel_id, column)


@router.get("/{funnel_id}/columns", response_model=List[ColumnReadWithCount])
async def get_column(funnel_id: int, db=Depends(AsyncDatabase.get_session)):
    columns = await KanbanRepository(db).get_columns(funnel_id)
    for column in columns:
        column.count = len(column.tasks)
    if not columns:
        raise HTTPException(status_code=404, detail="Column not found")
    return columns


@router.delete("/{funnel_id}/columns/{column_id}")
async def delete_column(funnel_id: int, column_id: int, db=Depends(AsyncDatabase.get_session)):
    funnel = await KanbanRepository(db).get(funnel_id)
    if not funnel:
        raise HTTPException(status_code=404, detail="Funnel not found")
    column = await KanbanRepository(db).get_column(column_id)
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")
    await KanbanRepository(db).delete_column(column_id)


@router.get("/{funnel_id}/columns/{column_id}", response_model=ColumnRead)
async def get_column(funnel_id: int, column_id: int, db=Depends(AsyncDatabase.get_session)):
    funnel = await KanbanRepository(db).get(funnel_id)
    if not funnel:
        raise HTTPException(status_code=404, detail="Funnel not found")
    column = await KanbanRepository(db).get_column(column_id)
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")
    return column


# tasks
@router.post("/columns/{column_id}/tasks", response_model=TaskRead, status_code=201)
async def create_task(column_id: int, task: TaskCreate, db=Depends(AsyncDatabase.get_session)):
    column = await KanbanRepository(db).get_column(column_id)
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")
    return await KanbanRepository(db).create_task(column_id, task)


@router.get("/columns/{column_id}/tasks", response_model=list[TaskRead])
async def get_tasks(column_id: int, db=Depends(AsyncDatabase.get_session)):
    column = await KanbanRepository(db).get_column(column_id)
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")
    return column.tasks


@router.put("/columns/{column_id}/tasks/{task_id}", response_model=TaskRead)
async def move_task(column_id: int, task_id: int, db=Depends(AsyncDatabase.get_session)):
    column = await KanbanRepository(db).get_column(column_id)
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")
    task = await KanbanRepository(db).get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return await KanbanRepository(db).move_task(task_id, column_id)
