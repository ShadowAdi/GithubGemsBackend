from __future__ import annotations  # Important for Python <3.10 for forward references

from pydantic import BaseModel
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.UserSchema import UserResponse
    from app.schemas.RepoSchema import RepoBase
else:
    UserResponse = None  # type: ignore
    RepoBase = None      # type: ignore


class CommentBase(BaseModel):
    id: int
    commentText: str
    commenterId: int
    postId: int
    parentId: Optional[int]

    class Config:
        from_attributes = True


class CommentCreate(BaseModel):
    commentText: str

    class Config:
        from_attributes = True


class CommentUpdate(BaseModel):
    commentText: str

    class Config:
        from_attributes = True


class CommentResponse(CommentBase):
    commentCommentedBy: Optional["UserResponse"]
    commentPostedOn: Optional["RepoBase"]
    replies: List["CommentResponse"] = []

    class Config:
        from_attributes = True


class CommentResponseWithMessage(BaseModel):
    message: str
    comment: CommentResponse

    class Config:
        from_attributes = True

