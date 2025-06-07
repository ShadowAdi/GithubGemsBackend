from fastapi import Depends, HTTPException
from app.schemas import UserUpdate
from sqlalchemy.orm import Session
from app.database import connect_db
from app.models import User
from typing import Optional, List
from app.config import logger
from app.utils import  hash_password


async def get_all_users(
    skip: int,
    limit: int,
    db: Session,
    name: Optional[str],
    email: Optional[str],
    languages: Optional[List[str]],  # Updated to List[str]
):
    try:
        query = db.query(User).offset(skip).limit(limit)
        if name:
            query = query.filter(User.username.ilike(f"%{name}%"))
        if email:
            query = query.filter(User.email.ilike(f"%{email}%"))
        if languages:
            query = query.filter(User.languages.overlap(languages))
        logger.info("All Users Have been fetched")
        return query.all()
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Something went wrong while fetching users."
        )


async def get_user(userId: int, db: Session):
    try:
        db_user = db.query(User).filter(User.id == userId).first()
        if not db_user:
            logger.error(f"User with id {userId} not found.")
            raise HTTPException(
                status_code=404, detail=f"User with ID {userId} not found"
            )
        logger.info(f"User with ID {userId} has been fetched successfully.")
        return db_user
    except Exception as e:
        logger.error(f"Unexpected error while fetching user {userId}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong while fetching user with ID {userId}",
        )


async def update_user(
    userId: int, userUpdate: UserUpdate, db: Session = Depends(connect_db)
):
    try:
        db_user = db.query(User).filter(User.id == userId).first()
        if not db_user:
            logger.error(f"Not Able To Find The User with this id: {str(userId)}")
            raise HTTPException(
                status_code=404,
                detail=f"Something Went Wrong  While Fetching User with Id: {str(userId)}",
            )
        for field, value in userUpdate.model_dump(exclude_unset=True).items():
            setattr(db_user, field, value)

        db.commit()
        db.refresh(db_user)
        logger.info(f"User Find With the Given Id: {str(userId)}")
        return db_user
    except Exception as e:
        logger.error(f"Not Able To update The User with this id: {str(userId)}")
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong while updating user with id: {str(userId)}",
        )


async def delete_user(userId: int, db: Session = Depends(connect_db)):
    try:
        userExit = db.query(User).filter(User.id == userId).first()
        if not userExit:
            logger.error(f"Failed to get the user with the id {str(userId)}. ")
            raise HTTPException(
                status_code=404,
                detail=f"Something Went Wrong  While Fetching User with Id: {str(userId)}",
            )
        db.delete(userExit)
        db.commit()
        logger.info("User Deleted Successfully")
        return {"success": True, "message": "User Deleted Successfully"}
    except Exception as e:
        logger.error(f"Not able to delete the user with id: {str(userId)}. Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong while deleting user with id: {str(userId)}",
        )


async def create_user(user: User, db: Session = Depends(connect_db)):
    try:
        hashed_password = hash_password(user.password)
        user_dict = user.model_dump()
        user_dict["password"] = hashed_password
        db_user = User(**user_dict)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.info("User Created Successfully")
        return db_user
    except Exception as e:
        logger.error("Failed To Created User")
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong while creating user.",
        )
