from typing import List

from fastapi import APIRouter, Depends
from database.base import AsyncDatabase
from database.repositories.StoryRepository import StoriesRepository
from database.models.stories import StoryCreate, StoryRead

router = APIRouter()


@router.post('/', name='create story', response_model=StoryRead)
async def create_story(story: StoryCreate, session=Depends(AsyncDatabase.get_session)):
    return await StoriesRepository(session).create(story.__dict__)


@router.get('/all', name='get all stories', response_model=List[StoryRead])
async def all_stories(session=Depends(AsyncDatabase.get_session)):
    return await StoriesRepository(session).all()


@router.get('/{story_id}', name='get story by id', response_model=StoryRead)
async def story_by_id(story_id: int, session=Depends(AsyncDatabase.get_session)):
    return await StoriesRepository(session).by_id(story_id)


@router.delete('/{story_id}', name='delete story by id')
async def del_story(story_id: int, session=Depends(AsyncDatabase.get_session)):
    return await StoriesRepository(session).delete(story_id)
