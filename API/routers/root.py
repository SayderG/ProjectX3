from fastapi import APIRouter
from database.base import AsyncDatabase
from database.models.users import Users

router = APIRouter()


@router.get('/', name='Root')
async def api_root():
    return "This is root API, documentation is available at /docs or /redoc"


@router.get("/db", name="Create database")
async def create_db():
    await AsyncDatabase.create_db()
    return "Database created"
