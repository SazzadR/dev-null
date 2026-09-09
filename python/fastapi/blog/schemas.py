from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(min_length=1, max_length=200)
    profile_picture_path: str = None


class UserProfilePicture(BaseModel):
    file_path: str


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=1, max_length=50)
    profile_picture_path: str | None = Field(default=None, min_length=1, max_length=200)


class UserResponse(UserBase):
    id: int


class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    content: str | None = Field(default=None, min_length=1)


class PostResponse(PostBase):
    id: int
    author: UserResponse
    date_posted: datetime


class EmptyResponse(BaseModel):
    pass


class ErrorResponse400(BaseModel):
    detail: str


class ErrorResponse404(BaseModel):
    detail: str
