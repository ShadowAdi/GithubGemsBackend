from fastapi import APIRouter, Depends, status
from app.schemas import RepoResponse, RepoCreate, RepoUpdate
from sqlalchemy.orm import Session
from app.dependency import get_current_user
from app.database import connect_db
from app.controllers import (
    create_repo_post,
    get_all_repos,
    get_repo,
    deleteRepo,
    updateRepo,
)

RepoRouter = APIRouter(prefix="/posts")


@RepoRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=RepoResponse)
async def create_repo(
    repo: RepoCreate,
    db: Session = Depends(connect_db),
    authenticateUser=Depends(get_current_user),
):

    return await create_repo_post(db=db, repoCreate=repo, userId=authenticateUser["id"])


@RepoRouter.get("/", status_code=status.HTTP_200_OK, response_model=list[RepoResponse])
async def get_repos(
    db: Session = Depends(connect_db),
    skip: int = 0,
    limit: int = 10,
):
    return await get_all_repos(db=db, limit=limit, skip=skip)


@RepoRouter.get(
    "/repo/{repoId}", status_code=status.HTTP_200_OK, response_model=RepoResponse
)
async def get_single_repo(repoId: int, db: Session = Depends(get_current_user)):
    return await get_repo(db=db, repoId=repoId)


@RepoRouter.patch(
    "/repo/{repoId}", status_code=status.HTTP_200_OK, response_model=RepoResponse
)
async def update_repo(
    repoId: int,
    db: Session = Depends(connect_db),
    authenticateUser=Depends(get_current_user),
    updatedRepo=RepoUpdate,
):
    return await updateRepo(
        db=db, repoId=repoId, userId=authenticateUser["userId"], postUpdate=updatedRepo
    )


@RepoRouter.delete(
    "/repo/{repoId}", status_code=status.HTTP_200_OK, response_model=dict
)
async def delete_repo(
    repoId: int,
    db: Session = Depends(connect_db),
    authenticateUser=Depends(get_current_user),
):
    return await deleteRepo(db=db, repoId=repoId, userId=authenticateUser["userId"])
