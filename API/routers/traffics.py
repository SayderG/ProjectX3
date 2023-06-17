from typing import List
from fastapi import APIRouter, Depends
from database.base import AsyncDatabase
from database.repositories.TrafficRepository import TrafficsRepository
from database.models.traffics import TrafficRead, TrafficCreate

router = APIRouter()


@router.post('/', name='store traffic', response_model=TrafficRead)
async def create_traffic(traffic: TrafficCreate, session=Depends(AsyncDatabase.get_session)):
    return await TrafficsRepository(session).create(traffic.__dict__)


@router.get('/all', name='get all traffic', response_model=List[TrafficRead])
async def all_traffics(session=Depends(AsyncDatabase.get_session)):
    return await TrafficsRepository(session).all()


@router.get('/{traffic_id}', name='get traffic by id', response_model=TrafficRead)
async def traffic_by_id(traffic_id: int, session=Depends(AsyncDatabase.get_session)):
    return await TrafficsRepository(session).by_id(traffic_id)


@router.delete('/{traffic_id}', name='delete traffic by id')
async def del_traffic(traffic_id: int, session=Depends(AsyncDatabase.get_session)):
    return await TrafficsRepository(session).delete(traffic_id)
