from pydantic import BaseModel, Field


class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    author: str
    date_posted: str
