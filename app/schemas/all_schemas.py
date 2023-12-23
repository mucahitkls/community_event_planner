from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


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


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    user_id: int
    event_id: int

    class Config:
        orm_mode = True
