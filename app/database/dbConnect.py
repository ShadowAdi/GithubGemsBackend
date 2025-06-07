import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config import logger

load_dotenv()

NEON_DB_URL = os.getenv("NEON_DB_URL")

if NEON_DB_URL is None:
    logger.error("Neon DB Url is not Exixt. Failed To Connect To DB")
    raise ValueError("NEON_DB_URL environment variable is missing")


engine = create_engine(NEON_DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def connect_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
