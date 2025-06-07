from app.database import Base
from sqlalchemy import Column, Integer, String, ARRAY, JSON, ForeignKey
from sqlalchemy.orm import relationship


class PostedRepos(Base):
    __tablename__ = "postedRepos"

    id = Column(Integer, primary_key=True, index=True)
    repoName = Column(String, nullable=False, index=True)
    repoDescription = Column(String, default="", index=False)
    repoPrimaryLanguage = Column(String, nullable=False, index=True)
    repoId = Column(Integer, nullable=False, index=True)
    repoCustomLabels = Column(ARRAY(String), default=list, index=True)
    repoHtmlUrl = Column(String, nullable=False)
    repoUrl = Column(String, nullable=False, index=True)
    repoTopics = Column(ARRAY(String), default=list)
    repoCloneUrl = Column(String, nullable=False)
    repoGitUrl = Column(String, nullable=False, index=True)
    repoOpenIssuesCount = Column(Integer, nullable=False)
    repoForksCount = Column(Integer, default=0)
    repoCustomTags = Column(ARRAY(String), default=list)
    repoOwner = Column(JSON, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    repoPostedBy = relationship("User", back_populates="postedRepos")

    comments = relationship("CommentModel", back_populates="commentPostedOn")

    upvotedUserIds = Column(ARRAY(Integer), default=list)
    downvotedUserIds = Column(ARRAY(Integer), default=list)

    upvotesCount = Column(Integer, default=0)
    downvotesCount = Column(Integer, default=0)
