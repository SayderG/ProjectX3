import datetime
from typing import List

from fastapi import APIRouter, Depends
from database.base import AsyncDatabase
from database.repositories.StreetRepository import StreetRepository
from database.models.streets import StreetCreate, StreetRead, StreetReadWithPredict

router = APIRouter()


@router.get('/predict', name='get predict', response_model=List[StreetReadWithPredict])
async def predict(date: datetime.datetime, session=Depends(AsyncDatabase.get_session)):
    return await StreetRepository(session).predict(date)


@router.get('/predict/{street_id}/month', name='predict on month')
async def predict_by_street_id(street_id: int, session=Depends(AsyncDatabase.get_session)):
    return await StreetRepository(session).predict_month(street_id)


@router.post('/', name='create street', response_model=StreetRead)
async def create_street(point: StreetCreate, session=Depends(AsyncDatabase.get_session)):
    return await StreetRepository(session).create(point.__dict__)


@router.get('/all', name='get all streets', response_model=List[StreetRead])
async def all_streets(session=Depends(AsyncDatabase.get_session)):
    return await StreetRepository(session).all()


@router.get('/{street_id}', name='get street by id', response_model=StreetRead)
async def street_by_id(street_id: int, session=Depends(AsyncDatabase.get_session)):
    return await StreetRepository(session).by_id(street_id)


@router.delete('/{street_id}', name='delete street by id')
async def del_street(street_id: int, session=Depends(AsyncDatabase.get_session)):
    return await StreetRepository(session).delete(street_id)
