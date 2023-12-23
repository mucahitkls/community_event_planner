from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    date_time: datetime
    location: str


class EventCreate(EventBase):
    pass


class Event(EventBase):
    id: int
    creator_id: int

    class Config:
        orm_mode = True
