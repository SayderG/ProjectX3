import datetime
from typing import Optional

from pydantic.types import condecimal
from sqlmodel import SQLModel, Field


class TrafficBase(SQLModel):
    longitude: condecimal(max_digits=18, decimal_places=3) = Field(default=0)
    latitude: condecimal(max_digits=18, decimal_places=3) = Field(default=0)
    date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    number_of_cars: int = Field(default=0)
    temperature: int


class Traffics(TrafficBase, table=True):
    id: Optional[int] = Field(primary_key=True)


class TrafficCreate(TrafficBase):
    pass


class TrafficRead(TrafficBase):
    id: int
