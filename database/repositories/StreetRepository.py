import datetime
from database.repositories.BaseRepository import BaseRepository
from database.models.streets import Streets, StreetReadWithPredict
from ML.app_predictions import get_prediction
import asyncio
from random import randint


class StreetRepository(BaseRepository):
    model = Streets

    async def predict(self, date: datetime.datetime):
        date = date.strftime('%Y-%m-%d %H:%M:%S')
        all_street = await self.all()
        temp = randint(15, 30)
        lst = []
        for i in all_street:
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
        for i in all_street:
            i = i.dict()
            for pred in predict_data:
                if i['street'] == pred['street']:
                    i['predictions'] = pred['predictions']
                    lst.append(i)
        return lst


if __name__ == '__main__':
    asyncio.run(main())
