from typing import List, Optional, TYPE_CHECKING
from pydantic import BaseModel, HttpUrl, Field

if TYPE_CHECKING:
    from app.schemas.UserSchema import UserResponse

class RepoCreate(BaseModel):
    repoUrl: str
    repoCustomLabels: Optional[List[str]] = []
    repoCustomTags: Optional[List[str]] = []
    repoTopics: Optional[List[str]] = []

    class Config:
        from_attributes = True

class RepoBase(BaseModel):
    id: int
    repoName: str
    repoDescription: Optional[str]
    repoPrimaryLanguage: Optional[str]
    repoId: int
    repoCustomLabels: Optional[List[str]]
    repoHtmlUrl: Optional[str]
    repoUrl: HttpUrl
    repoCloneUrl: HttpUrl
    repoGitUrl: str
    repoOpenIssuesCount: int
    repoForksCount: int
    repoCustomTags: Optional[List[str]]
    repoOwner: dict
    upvotedUserIds: Optional[List[int]] = []
    downvotedUserIds: Optional[List[int]] = []
    upvotesCount: int
    downvotesCount: int
    user_id: int = Field(...)

    class Config:
        from_attributes = True

class RepoResponse(RepoBase):
    repoPostedBy: "UserResponse"  # Forward reference using string

    class Config:
        from_attributes = True

class RepoUpdate(BaseModel):
    repoDescription: Optional[str]
    repoCustomLabels: Optional[List[str]]
    repoTopics: Optional[List[str]]
    repoCustomTags: Optional[List[str]]

    class Config:
        from_attributes = True