from typing import List

from fastapi import APIRouter, Depends
from database.base import AsyncDatabase
from database.repositories.PointRepository import PointsRepository
from database.models.points import PointCreate, PointRead

router = APIRouter()


@router.post('/', name='create point', response_model=PointRead)
async def create_point(point: PointCreate, session=Depends(AsyncDatabase.get_session)):
    return await PointsRepository(session).create(point.__dict__)


@router.get('/all', name='get all points', response_model=List[PointRead])
async def all_points(session=Depends(AsyncDatabase.get_session)):
    return await PointsRepository(session).all()


@router.get('/{point_id}', name='get point by id', response_model=PointRead)
async def point_by_id(point_id: int, session=Depends(AsyncDatabase.get_session)):
    return await PointsRepository(session).by_id(point_id)


@router.delete('/{point_id}', name='delete point by id', response_model=PointRead)
async def del_point(point_id: int, session=Depends(AsyncDatabase.get_session)):
    return await PointsRepository(session).delete(point_id)
