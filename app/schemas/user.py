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