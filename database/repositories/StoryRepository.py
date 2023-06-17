from database.repositories.BaseRepository import BaseRepository
from database.models.stories import Stories


class StoriesRepository(BaseRepository):
    model = Stories
