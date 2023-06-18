import datetime
from geoalchemy2 import Geometry
from typing import Optional, Any, List
from sqlmodel import SQLModel, Field, Column, ARRAY, NUMERIC
from pydantic import condecimal, validator
from fastapi import HTTPException


class PointBase(SQLModel):
    point: List[List[condecimal(max_digits=18, decimal_places=15)]] = Field(sa_column=Column(ARRAY(NUMERIC, dimensions=2)))
    type: str
    radius: int = Field(default=0)
    description: str = Field(max_length=64)
    fromTime: datetime.datetime = Field(default_factory=datetime.datetime.now)
    toTime: datetime.datetime = Field(default_factory=datetime.datetime.now)


class Points(PointBase, table=True):
    id: Optional[int] = Field(primary_key=True)


class PointCreate(PointBase):
    @validator('type')
    def validate_type(cls, value):
        if value.lower() in ['alert', 'critical', 'normal', 'simple']:
            return value.lower()
        else:
            raise HTTPException(404, detail='most be only alert, critical, normal or simple')


class PointRead(PointBase):
    id: int
