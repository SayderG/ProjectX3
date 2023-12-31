import datetime
from typing import Optional, List

from pydantic.types import condecimal
from sqlmodel import SQLModel, Field, Column, ARRAY, NUMERIC


class TrafficBase(SQLModel):
    point: List[List[condecimal(max_digits=18, decimal_places=15)]] = Field(sa_column=Column(ARRAY(NUMERIC, dimensions=2)))
    date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    number_of_cars: int = Field(default=0)
    temperature: int


class Traffics(TrafficBase, table=True):
    id: Optional[int] = Field(primary_key=True)


class TrafficCreate(TrafficBase):
    pass


class TrafficRead(TrafficBase):
    id: int
