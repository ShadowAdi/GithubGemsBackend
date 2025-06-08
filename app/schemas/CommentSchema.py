from pydantic import BaseModel, Field
from typing import List, Optional, TYPE_CHECKING
from app.schemas.UserSchema import UserResponse
from app.schemas.RepoSchema import RepoBase

if TYPE_CHECKING:
    from app.schemas.UserSchema import UserResponse
    from app.schemas.RepoSchema import RepoBase


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
    postId: int
    parentId: Optional[int] = None

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


class RepoResponseWithMessage(BaseModel):
    message: str
    comment: CommentResponse

    class Config:
        from_attributes = True


CommentResponse.update_forward_refs()
