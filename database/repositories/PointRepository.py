from database.repositories.BaseRepository import BaseRepository
from database.models.points import Points


class PointsRepository(BaseRepository):
    model = Points
