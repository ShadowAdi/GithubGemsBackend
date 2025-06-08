from fastapi import HTTPException
from app.schemas import CommentUpdate, CommentResponse, CommentCreate
from app.config import logger
from app.models import PostedRepos, User, CommentModel
from sqlalchemy.orm import Session, joinedload


async def create_comment(postId: int, commentText: str, db: Session, userId: int):
    try:
        if not postId:
            logger.error(f"Failed to get the postId for a comment")
            raise HTTPException(
                status_code=403, detail=f"Failed to get the postId for a comment"
            )
        if not userId:
            logger.error(f"User Id Don't Exist")
            raise HTTPException(
                status_code=403, detail=f"User with ID {userId} not found"
            )
        repoFind = db.query(PostedRepos).filter(PostedRepos.id == postId).first()
        if not repoFind:
            logger.error(f"Repo with id {postId} not found.")
            raise HTTPException(
                status_code=403, detail=f"Repo with ID {postId} not found"
            )
        userFind = db.query(User).filter(User.id == userId).first()
        if not userFind:
            logger.error(f"User with id {userId} not found.")
            raise HTTPException(
                status_code=403, detail=f"User with ID {userId} not found"
            )
        commentCreated = CommentModel(
            commentText=commentText, postId=postId, commenterId=userId
        )
        db.add(commentCreated)
        db.commit()
        db.refresh(commentCreated)
        return commentCreated

    except Exception as e:
        logger.error(
            f"Failed to create comment for the given postId {str(postId)} and the error is: {str(e)}"
        )
        raise HTTPException(
            status_code=403,
            detail=f"Failed to create comment for the given postId {str(postId)} and the error is: {str(e)}",
        )
