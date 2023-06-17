from fastapi import APIRouter
from Maps.map import create_map

router = APIRouter()


@router.get('/', name='get map')
async def get_map(place: str):
    return create_map(place)
