from fastapi import APIRouter, Depends, Query
from app.schemas import UserResponse, UserUpdate, UserCreation
from sqlalchemy.orm import Session
from app.database import connect_db
from typing import Optional, Annotated, List
from app.controllers import create_user,delete_user,get_all_users,get_user,update_user
from pydantic import Field, BaseModel
from app.database import connect_db
from app.dependency import get_current_user

UserRouter = APIRouter(prefix="/users")


class FilterParams(BaseModel):
    skip: int = Field(0)
    limit: int = Field(10, gt=1, le=100)
    name: Optional[str] = None  # Explicitly optional, default None
    email: Optional[str] = None  # Explicitly optional, default None
    languages: Optional[List[str]] = None  # Optional list of strings


@UserRouter.get("/", response_model=list[UserResponse])
async def getAllUsers(
    filter_query: Annotated[FilterParams, Query()], db: Session = Depends(connect_db)
):
    return await get_all_users(
        skip=filter_query.skip,
        limit=filter_query.limit,
        db=db,
        email=filter_query.email,
        languages=filter_query.languages,
        name=filter_query.name,
    )


@UserRouter.get("/user/{userId}", response_model=UserResponse)
async def getSingleUser(userId: int, db: Session = Depends(connect_db)):
    return await get_user(userId=userId, db=db)


@UserRouter.patch("/user")
async def updateSingleUser(
    user: UserUpdate,
    db: Session = Depends(connect_db),
    authenticateUser=Depends(get_current_user),
):
    return await update_user(
        userId=authenticateUser["id"], db=db, userUpdate=user
    )


@UserRouter.delete("/user")
async def deleteSingleUser(
    db: Session = Depends(connect_db), user=Depends(get_current_user)
):
    return await delete_user(userId=user["id"], db=db)


@UserRouter.post("/", response_model=UserResponse)
async def createUser(user: UserCreation, db: Session = Depends(connect_db)):
    return await create_user(user=user, db=db)
