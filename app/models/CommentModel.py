from app.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class CommentModel(Base):
    __tablename__ = "repoComments"

    id = Column(Integer, primary_key=True, index=True)
    commentText = Column(String, nullable=False)

    commenterId = Column(Integer, ForeignKey("users.id"), nullable=False)
    commentCommentedBy = relationship("User", back_populates="comments")

    postId = Column(Integer, ForeignKey("postedRepos.id"), nullable=False)
    commentPostedOn = relationship("PostedRepos", back_populates="comments")

    parentId=Column(Integer,ForeignKey("repoComments.id"),nullable=False)
    replies=relationship("CommentModel",backref="parent",remote_side=[id])
