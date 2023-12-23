from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    class Config:
        orm_mode = True


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
