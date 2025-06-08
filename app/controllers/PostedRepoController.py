from fastapi import Depends, HTTPException
from app.schemas import RepoResponse, RepoCreate, RepoUpdate
from sqlalchemy.orm import Session
from app.api import GetRepoInfoUrl
from app.config import logger
from app.utils import extract_owner_repo
from app.models import PostedRepos, User


from sqlalchemy.orm import Session, joinedload
from fastapi import Depends, HTTPException
from app.schemas import RepoResponse, RepoCreate, RepoUpdate
from app.models import PostedRepos, User
from app.api import GetRepoInfoUrl
from app.config import logger
from app.utils import extract_owner_repo


async def create_repo_post(
    db: Session,
    repoCreate: RepoCreate,
    userId: int,
) -> RepoResponse:  # Specify return type
    try:
        db_user = db.query(User).filter(User.id == userId).first()
        if not db_user:
            logger.error(f"Not Able To Find The User with this id: {str(userId)}")
            raise HTTPException(
                status_code=404,
                detail=f"Something Went Wrong While Fetching User with Id: {str(userId)}",
            )

        repoOwnerName, repoName = extract_owner_repo(repoUrl=repoCreate.repoUrl)

        github_data = await GetRepoInfoUrl(
            repoName=repoName, repoOwnerName=repoOwnerName
        )
        repoFind = (
            db.query(PostedRepos)
            .filter(PostedRepos.repoName == github_data["name"])
            .first()
        )
        if repoFind:
            logger.error(f"Repo already exists.")
            raise HTTPException(
                status_code=407,
                detail=f"Repo with repo name {github_data["name"]} already exists",
            )

        repo_model = PostedRepos(
            repoName=github_data["name"],
            repoDescription=github_data["description"],
            repoPrimaryLanguage=github_data["language"],
            repoId=github_data["id"],
            repoCustomLabels=repoCreate.repoCustomLabels,
            repoUrl=github_data["url"],
            repoHtmlUrl=github_data[
                "html_url"
            ],  # Fixed: was incorrectly set to "description"
            repoCloneUrl=github_data["clone_url"],
            repoGitUrl=github_data["git_url"],
            repoOpenIssuesCount=github_data["open_issues_count"],
            repoForksCount=github_data["forks_count"],
            repoCustomTags=repoCreate.repoCustomTags,
            repoOwner=github_data["owner"],
            repoTopics=repoCreate.repoTopics,
            user_id=userId,
        )
        db.add(repo_model)
        db.commit()
        db.refresh(repo_model)

        # Eagerly load the repoPostedBy relationship
        repo_model = (
            db.query(PostedRepos)
            .options(joinedload(PostedRepos.repoPostedBy))
            .filter(PostedRepos.id == repo_model.id)
            .first()
        )

        return repo_model  # FastAPI will handle conversion to RepoResponse
    except Exception as e:
        logger.error(
            f"Failed to post repo which has the repo url of {str(repoCreate.repoUrl)} and the error is {str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong while posting repo with {str(repoCreate.repoUrl)} and the error is {str(e)}",
        )


async def get_all_repos(db: Session, skip: int, limit: int):
    try:
        query = db.query(PostedRepos).offset(skip).limit(limit)
        logger.info("All Repos Have been fetched")
        return query.all()
    except Exception as e:
        logger.error(f"Error fetching repo posts: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong while fetching repo posts. {str(e)}",
        )


async def get_repo(db: Session, repoId: int):
    try:
        repoFind = db.query(PostedRepos).filter(PostedRepos.id == repoId).first()
        if not repoFind:
            logger.error(f"Repo with id {repoId} not found.")
            raise HTTPException(
                status_code=404, detail=f"Repo with ID {repoId} not found"
            )
        logger.info(f"Repo With Id: {str(repoId)} has been fetched successfully")
        return repoFind
    except Exception as e:
        logger.error(f"Error fetching repo posts: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong while fetching repo posts. {str(e)}",
        )


async def updateRepo(db: Session, repoId: int, userId: int, postUpdate: RepoUpdate):
    try:
        if not repoId:
            logger.error(f"Repo Id Don't Exist")
            raise HTTPException(
                status_code=403, detail=f"Repo with ID {repoId} not found"
            )
        if not userId:
            logger.error(f"User Id Don't Exist")
            raise HTTPException(
                status_code=403, detail=f"User with ID {userId} not found"
            )
        repoFind = db.query(PostedRepos).filter(PostedRepos.id == repoId).first()
        if not repoFind:
            logger.error(f"Repo with id {repoId} not found.")
            raise HTTPException(
                status_code=403, detail=f"Repo with ID {repoId} not found"
            )
        if repoFind.user_id != userId:
            logger.error(f"{str(userId)} This Id is not the creator of post.")
            raise HTTPException(
                status_code=403, detail=f"You Are Not Authenticated to update the post"
            )
        for field, value in postUpdate.model_dump(exclude_unset=True).items():
            setattr(repoFind, field, value)
        db.commit()
        db.refresh(repoFind)
        logger.info(f"Repo With Id: {str(repoId)} has been updated successfully")
        return repoFind
    except Exception as e:
        logger.error(f"Error update repo posts with id {str(repoId)}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong while updating repo posts. {str(e)}",
        )


async def deleteRepo(db: Session, repoId: int, userId: int):
    try:
        if not repoId:
            logger.error(f"Repo Id Don't Exist")
            raise HTTPException(
                status_code=403, detail=f"Repo with ID {repoId} not found"
            )
        if not userId:
            logger.error(f"User Id Don't Exist")
            raise HTTPException(
                status_code=403, detail=f"User with ID {userId} not found"
            )
        repoFind = db.query(PostedRepos).filter(PostedRepos.id == repoId).first()
        if not repoFind:
            logger.error(f"Repo with id {repoId} not found.")
            raise HTTPException(
                status_code=403, detail=f"Repo with ID {repoId} not found"
            )
        if repoFind.user_id != userId:
            logger.error(f"{str(userId)} This Id is not the creator of post.")
            raise HTTPException(
                status_code=403, detail=f"You Are Not Authenticated to update the post"
            )
        db.delete(repoFind)
        db.commit()
        logger.info(f"Repo With Id: {str(repoId)} has been deleted successfully")
        return {"success": True, "message": "Repo has been deleted", "status_code": 200}
    except Exception as e:
        logger.error(f"Error delete repo posts with id {str(repoId)}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong while deleting repo posts. {str(e)}",
        )
