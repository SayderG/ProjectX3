import datetime
from typing import Optional, List
from pydantic.types import condecimal
from sqlmodel import SQLModel, Field, Column, ARRAY, NUMERIC


class StreetBase(SQLModel):
    point: List[List[condecimal(max_digits=18, decimal_places=15)]] = Field(sa_column=Column(ARRAY(NUMERIC, dimensions=2)))
    street: str = Field(unique=True)


class StreetPredict(SQLModel):
    date: datetime.datetime = Field(default_factory=datetime.datetime.now)


class Streets(StreetBase, table=True):
    id: Optional[int] = Field(primary_key=True)


class StreetCreate(StreetBase):
    pass


class StreetRead(StreetBase):
    id: int

class StreetReadWithPredict(StreetRead):
    predictions: float