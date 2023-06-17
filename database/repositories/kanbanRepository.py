from sqlalchemy import select
from database.models.funnels import Funnels, FunnelCreate
from database.models.columns import Columns, ColumnCreate
from database.models.task_detail import Tasks_detail
from database.models.tasks import Tasks, TaskCreate
from database.repositories.BaseRepository import BaseRepository


class KanbanRepository(BaseRepository):
    model = Funnels

    # funnels
    async def create(self, funnel: FunnelCreate):
        funnel = self.model(name=funnel.name,
                            columns=[Columns(title="To Do"), Columns(title="In Progress"), Columns(title="Done")])
        self.session.add(funnel)
        await self.session.commit()
        return funnel

    async def get(self, funnel_id: int):
        return await self.session.get(self.model, funnel_id)

    async def all(self):
        query = await self.session.execute(select(self.model))
        return query.scalars().all()

    # columns
    async def create_column(self, funnel_id: int, data: ColumnCreate):
        column = Columns(**data.__dict__, funnel_id=funnel_id)
        self.session.add(column)
        await self.session.commit()
        return column

    async def get_column(self, column_id: int):
        return await self.session.get(Columns, column_id)

    async def get_columns(self, funnel_id: int):
        query = await self.session.execute(select(Columns).where(Columns.funnel_id == funnel_id).order_by(Columns.id))
        result = query.scalars().all()
        print(result)
        return result

    async def delete_column(self, column_id: int):
        column = await self.session.get(Columns, column_id)
        await self.session.delete(column)
        await self.session.commit()
        return column

    async def update_column(self, column_id: int, data: dict):
        column = await self.session.get(Columns, column_id)
        column.title = data['title']
        await self.session.commit()
        return column

    # tasks

    async def create_task(self, column_id: int, data: TaskCreate):
        task = Tasks(**data.__dict__, column_id=column_id, detail=[Tasks_detail()])
        self.session.add(task)
        await self.session.commit()
        return task

    async def del_task(self, task_id: int):
        task = await self.session.get(Tasks, task_id)
        await self.session.delete(task)
        await self.session.commit()

    async def update_task(self, task_id: int, data: dict):
        task = await self.session.get(Tasks, task_id)
        for key, value in data.__dict__.items():
            if value is not None:
                setattr(data, key, value)
        await self.session.commit()
        return task

    async def move_task(self, task_id: int, column_id: int):
        task = await self.session.get(Tasks, task_id)
        task.column_id = column_id
        await self.session.commit()
        return task

    async def get_task(self, task_id):
        task = await self.session.get(Tasks, task_id)
        return task
