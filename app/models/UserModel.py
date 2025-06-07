from app.database import Base
from sqlalchemy import Column, Integer, String, ARRAY
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=False)
    email = Column(String, index=True, nullable=False)
    password = Column(String, index=True, nullable=False, unique=True)
    languages = Column(ARRAY(String), default=list)

    postedRepos = relationship("PostedRepos", back_populates="repoPostedBy")
    comments = relationship("CommentModel", back_populates="commentCommentedBy")
