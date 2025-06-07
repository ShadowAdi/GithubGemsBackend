from fastapi import APIRouter, Depends
from app.schemas import AuthResponse, LoginUserData, UserResponse
from sqlalchemy.orm import Session
from app.database import connect_db
from app.controllers import LoginUser, getAuthenticatedUser
from app.dependency import get_current_user

AuthRouter = APIRouter(prefix="/auth")

@AuthRouter.post("/login", response_model=AuthResponse)
async def login_user(
    login_user: LoginUserData,
    db: Session = Depends(connect_db),
):
    return await LoginUser(email=login_user.email, password=login_user.password, db=db)

@AuthRouter.get("/me", response_model=UserResponse)
async def get_me_user(
    db: Session = Depends(connect_db),
    user=Depends(get_current_user),
):
    user_obj = await getAuthenticatedUser(db=db, userId=user["id"])
    return user_obj