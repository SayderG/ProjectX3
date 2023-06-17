import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import condecimal, validator
from fastapi import HTTPException


class StoryBase(SQLModel):
    title: str
    subtitle: str
    type: str
    description: str
    created_ad: datetime.datetime = Field(default_factory=datetime.datetime.now)
    active: bool = Field(default=True)


class Stories(StoryBase, table=True):
    id: Optional[int] = Field(primary_key=True)


class StoryCreate(StoryBase):
    @validator('type')
    def validate_type(cls, value):
        if value.lower() in ['important', 'interesting', 'simple']:
            return value.lower()
        else:
            raise HTTPException(404, detail='most be only important, interesting or simple')


class StoryRead(StoryBase):
    id: int
