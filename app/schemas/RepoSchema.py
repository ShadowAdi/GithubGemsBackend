from pydantic import BaseModel, HttpUrl
from .UserSchema import UserResponse
from typing import List, Optional


class RepoCreate(BaseModel):
    repoUrl: str
    repoCustomLabels: Optional[List[str]] = []
    repoCustomTags: Optional[List[str]] = []
    repoTopics: Optional[List[str]] = []

    class Config:
        orm_mode = True


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
    userId:int

    class Config:
        orm_mode = True


class RepoResponse(RepoBase):
    repoPostedBy: UserResponse


class RepoUpdate(BaseModel):
    repoDescription: Optional[str] = None
    repoCustomLabels: Optional[List[str]] = None
    repoTopics: Optional[List[str]] = None
    repoCustomTags: Optional[List[str]] = None
