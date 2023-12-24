from pydantic import BaseModel


class CommentBase(BaseModel):
    content: str
    event_id: int


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

