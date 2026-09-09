from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(min_length=1, max_length=200)


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int


class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    author: str
    date_posted: str


class ErrorResponse400(BaseModel):
    detail: str


class ErrorResponse404(BaseModel):
    detail: str
