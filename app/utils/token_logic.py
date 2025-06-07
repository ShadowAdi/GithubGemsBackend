from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt,ExpiredSignatureError
from sqlalchemy.orm import Session
from app.database import connect_db
from dotenv import load_dotenv
from app.config import logger 
import os

load_dotenv()

HASH_SECRET = "56dd0b4efdced622b9f648243af666d4420ed685b85c9c8adc45cb810d8caf4a62188bf80bf67cd70d712a344730bad594d8760772798eab4fc2c5d5859fb402"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3600
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})  # ✅ use `exp` and no strftime
    encoded_jwt = jwt.encode(to_encode, HASH_SECRET, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, HASH_SECRET, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        logger.error("Token Is Expired")
        print("Token has expired")
        return None
    except JWTError as e:
        logger.error(f"Token Is Expired {str(e)}")
        print("JWTError:", str(e))
        return None
