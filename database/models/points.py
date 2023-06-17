from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import condecimal, validator
from fastapi import HTTPException


class PointBase(SQLModel):
    longitude: condecimal(max_digits=18, decimal_places=3) = Field(default=0)
    latitude: condecimal(max_digits=18, decimal_places=3) = Field(default=0)
    type: str
    radius: int = Field(default=0)
    description: str = Field(max_length=64)


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
