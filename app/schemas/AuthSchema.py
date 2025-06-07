from typing import Optional
from pydantic import BaseModel


class AuthResponse(BaseModel):
    token: str
    userId: int
    email: str
    token_type: str
    success: bool

    class config:
        orm_mode = True


class LoginUserData(BaseModel):
    email: str
    password: str

    class config:
        orm_mode = True
