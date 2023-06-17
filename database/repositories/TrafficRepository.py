from database.repositories.BaseRepository import BaseRepository
from database.models.traffics import Traffics


class TrafficsRepository(BaseRepository):
    model = Traffics
