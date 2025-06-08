from typing import List, Optional, TYPE_CHECKING
from pydantic import BaseModel, Field, EmailStr

if TYPE_CHECKING:
    from app.schemas.RepoSchema import RepoResponse

class UserSchema(BaseModel):
    username: str = Field(..., min_length=3)
    email: EmailStr

    class Config:
        from_attributes = True

class UserCreation(UserSchema):
    password: str
    languages: List[str]

    class Config:
        from_attributes = True

class UserResponse(UserSchema):
    id: int
    languages: List[str]
    comments: List[int]
    postedRepos: List["RepoBase"]  # Forward reference using string - import RepoBase if needed

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    languages: Optional[List[str]]

    class Config:
        from_attributes = True