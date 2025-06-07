from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional


class UserSchema(BaseModel):
    username: str = Field(..., min_length=3)
    email: EmailStr
    class config:
        orm_mode=True


class UserCreation(UserSchema):
    password: str = Field(...)
    languages: List[str]


class UserResponse(UserSchema):
    id: int
    languages: List[str]
    postedRepos: List[int]
    comments: List[int]
    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    languages: Optional[list[str]] = None
