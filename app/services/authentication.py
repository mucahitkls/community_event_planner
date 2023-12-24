"""
This module handles user authentication for the FastAPI application, including password verification,
token generation, and user authentication based on tokens.

It utilizes the Passlib library for password hashing and the python-jose library for creating and verifying JWT tokens.
"""

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
    """
        Verify a password against a hashed version.

        Args:
            plain_password (str): The plain text password to verify.
            hashed_password (str): The hashed password to compare against.

        Returns:
            bool: True if the password is correct, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
        Hash a password using bcrypt.

        Args:
            password (str): The plain text password to hash.

        Returns:
            str: The hashed password.
    """
    return pwd_context.hash(password)


def authenticate_user(db: Session, username: str, password: str):
    """
        Authenticate a user by username and password.

        Args:
            db (Session): The database session to use for the operation.
            username (str): The username of the user to authenticate.
            password (str): The password of the user to authenticate.

        Returns:
            User: The authenticated User object, or False if authentication failed.
    """
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
        Create a JWT access token.

        Args:
            data (dict): The data to encode in the token (e.g., the username).
            expires_delta (Optional[timedelta], optional): The time delta in which the token will expire.

        Returns:
            str: The encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """
        Decode a JWT token.

        Args:
            token (str): The JWT token to decode.

        Returns:
            Optional[dict]: The decoded token data, or None if the token is invalid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> UserInDB:
    """
       Retrieve the current user based on the JWT token.

       Args:
           db (Session): The database session to use for the operation.
           token (str): The JWT token to authenticate.

       Raises:
           HTTPException: 401 error if the token is invalid or the user does not exist.

       Returns:
           UserInDB: The authenticated User object.
    """
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
