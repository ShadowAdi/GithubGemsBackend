from fastapi import APIRouter, Depends, status, Body
from sqlalchemy.orm import Session
from app.dependency import get_current_user
from app.database import connect_db
from app.schemas import (
    CommentResponse,
    CommentCreate,
    CommentUpdate,
    CommentResponseWithMessage,
)
from app.controllers import create_comment

CommentRouter = APIRouter(prefix="/comments")


@CommentRouter.get(
    "/{postId}", status_code=status.HTTP_200_OK, response_model=list[CommentResponse]
)
async def get_comments(postId: int, db: Session = Depends(connect_db)):
    pass


@CommentRouter.post(
    "/{postId}", status_code=status.HTTP_201_CREATED, response_model=CommentCreate
)
async def create_comment_route(
    postId: int,
    comment: CommentCreate,
    db: Session = Depends(connect_db),
    authenticateUser=Depends(get_current_user),
):
    return await create_comment(
        postId=postId,
        commentText=comment.commentText,
        db=db,
        userId=authenticateUser["id"],
    )


@CommentRouter.get(
    "/comment/{postId}/{commentId}",
    status_code=status.HTTP_200_OK,
    response_model=CommentResponse,
)
async def get_single_comment(
    postId: int, commentId: int, db: Session = Depends(connect_db)
):
    pass


@CommentRouter.patch(
    "/comment/{postId}/{commentId}",
    status_code=status.HTTP_200_OK,
    response_model=CommentUpdate,
)
async def update_single_comment(
    postId: int,
    commentId: int,
    comment: CommentUpdate,
    db: Session = Depends(connect_db),
    authenticateUser=Depends(get_current_user),
):

    pass


@CommentRouter.delete(
    "/comment/{postId}/{commentId}",
    status_code=status.HTTP_200_OK,
    response_model=CommentResponseWithMessage,
)
async def delete_single_comment(
    postId: int, commentId: int, db: Session = Depends(connect_db)
):
    pass
