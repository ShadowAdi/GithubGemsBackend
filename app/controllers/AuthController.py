from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models import User
from app.config import logger
from app.utils import verify_password,create_access_token


async def LoginUser(email: str, password: str, db: Session):
    try:
        findUser = db.query(User).filter(User.email == email).first()
        if not findUser:
            logger.error(f"User With email {email} not found.")
            raise HTTPException(
                status_code=404, detail=f"User With email {email} not found."
            )
        find_user_dict = findUser.__dict__
        isVerified = verify_password(
            password=password, hashed_password=find_user_dict["password"]
        )
        if not isVerified:
            logger.error(f"Wrong Password! This is  the given password {password}.")
            raise HTTPException(status_code=404, detail="Invalid Credentials")
        token = create_access_token(
            data={"sub": str(find_user_dict["id"]), "email": find_user_dict["email"]}
        )
        return {
            "token": token,
            "token_type": "bearer",
            "userId": find_user_dict["id"],
            "email": find_user_dict["email"],
            "success": True,
        }

    except Exception as e:
        logger.error(f"Error login user: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Something went wrong while  login user"
        )


async def getAuthenticatedUser(userId: int, db: Session):
    try:
        if not userId:
            logger.error(f"User Not Found.")
            raise HTTPException(status_code=404, detail=f"User Not Found.")

        findUser = db.query(User).filter(User.id == userId).first()
        if not findUser:
            logger.error(f"Authenticated User Not Found.")
            raise HTTPException(
                status_code=404, detail=f"Authenticated User Not Found."
            )
        logger.info("Authenticated User Found")
        return {
            "id": findUser.id,
            "username": findUser.username,
            "email": findUser.email,
            "languages": findUser.languages,
            "postedRepos": findUser.postedRepos,
            "comments": findUser.comments,
        }
    except Exception as e:
        logger.error(f"Error login user: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Something went wrong while  getting login user"
        )
