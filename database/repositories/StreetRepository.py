import datetime

from fastapi import HTTPException

from database.repositories.BaseRepository import BaseRepository
from database.models.streets import Streets, StreetReadWithPredict
from ML.app_predictions import get_prediction
import asyncio
from random import randint


class StreetRepository(BaseRepository):
    model = Streets

    async def predict(self, date: datetime.datetime, street_id: int = None):
        date = date.strftime('%Y-%m-%d %H:%M:%S')
        if street_id is None:
            streets = await self.all()
        else:
            streets = await self.by_id(street_id)
            if streets is None:
                raise HTTPException(status_code=404, detail="Street not found")
            streets = [streets]
        temp = randint(15, 30)
        lst = []
        for i in streets:
            i = i.dict()
            i['date'] = date
            i['latitude'] = float(i['point'][0][0])
            i['longitude'] = float(i['point'][0][1])
            i['temperature'] = temp
            i.pop('point')
            i.pop('id')
            lst.append(i)
        values = [i.values() for i in lst]
        columns = lst[0].keys()
        predict = get_prediction(values, columns)
        predict_data = predict.to_dict(orient='records')
        lst = []
        for i in streets:
            i = i.dict()
            for pred in predict_data:
                if i['street'] == pred['street']:
                    i['predictions'] = pred['predictions']
                    if street_id is not None:
                        i['date'] = date
                    lst.append(i)
        return lst

    async def predict_month(self, street_id: int):
        curr_date = datetime.datetime.now()
        lst = [await self.predict(curr_date + datetime.timedelta(days=i), street_id) for i in range(1, 30)]
        return lst
