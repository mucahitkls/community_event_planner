from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
from app.services.database import get_db
from .crud_user import get_user_by_email, get_user_by_username
from app.models.user import User
from app.schemas.user import UserInDB

from dotenv import load_dotenv
import os

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


# async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> UserInDB:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"}
#     )
#     print("here")
#     payload = decode_token(token)
#     if payload is None:
#         raise credentials_exception
#     username: str = payload.get('sub')
#     print(f"username")
#
#     if username is None:
#         raise credentials_exception
#     user = get_user_by_username(db=db, username=username)
#     if user is None:
#         raise credentials_exception
#     return user


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    logger.info("Attempting to authenticate user")
    payload = decode_token(token)

    if payload is None:
        logger.warning("Token payload could not be decoded")
        raise credentials_exception

    username: str = payload.get('sub')

    if username is None:
        logger.warning("Username not found in token payload")
        raise credentials_exception

    user = get_user_by_username(db=db, username=username)

    if user is None:
        logger.warning(f"User with username {username} not found")
        raise credentials_exception

    logger.info(f"User {username} successfully authenticated")
    return user
