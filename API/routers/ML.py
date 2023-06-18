from fastapi import APIRouter, Depends
from ML.app_training import generate_model

router = APIRouter()


@router.post('/', name='gen model')
async def create_model():
    return generate_model()
