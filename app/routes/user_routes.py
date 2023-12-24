from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas import user as user_schema
from app.services import crud_user, authentication
from app.services.database import get_db

router = APIRouter(
    prefix='/users',
    tags=["users"],
    responses={404: {"description": "Not found"}}
)


@router.post("/register", response_model=user_schema.User)
async def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    """
        Register a new user.

        This endpoint allows anyone to register a new user with a username and password. It checks if the username already exists and, if not, creates a new user.

        Args:
            user (UserCreate): The user information including username and password.
            db (Session, optional): The database session dependency.

        Raises:
            HTTPException: 400 error if the username is already taken.

        Returns:
            User: The newly created User object with public information.
    """
    db_user = crud_user.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud_user.create_user(db=db, user=user)


@router.get("/", response_model=List[user_schema.User])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
        Retrieve a list of all registered users with optional pagination.

        Args:
            skip (int, optional): The number of items to skip before starting to collect the result set.
            limit (int, optional): The maximum number of items to return.
            db (Session, optional): The database session dependency.

        Returns:
            List[User]: A list of User objects.
    """
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=user_schema.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    """
        Retrieve a specific user by their user ID.

        Args:
            user_id (int): The unique identifier of the user to retrieve.
            db (Session, optional): The database session dependency.

        Raises:
            HTTPException: 404 error if the user is not found.

        Returns:
            User: The requested User object if found.
    """
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{user_id}", response_model=user_schema.User)
async def update_user(user_id: int, user: user_schema.UserCreate, db: Session = Depends(get_db)):
    """
        Update an existing user's information.

        Args:
            user_id (int): The ID of the user to update.
            user (UserCreate): The updated user information.
            db (Session, optional): The database session dependency.

        Returns:
            User: The updated User object if the operation was successful.
    """

    return crud_user.update_user(db=db, user_id=user_id, user=user)


@router.delete("/{user_id}", response_model=user_schema.User)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
        Delete a user by their user ID.

        Args:
            user_id (int): The unique identifier of the user to delete.
            db (Session, optional): The database session dependency.

        Returns:
            User: The deleted User object if the operation was successful.
    """
    return crud_user.delete_user(db=db, user_id=user_id)


@router.post("/login")
async def login(user: user_schema.UserLogin, db: Session = Depends(get_db)):
    """
        Authenticate a user and provide an access token for future requests.
        This endpoint verifies the user's credentials and, if valid, generates a new access token for the user.

        Args:
            user (UserLogin): The user's login information including username and password.
            db (Session, optional): The database session dependency.

        Raises:
            HTTPException: 401 error if the username or password is incorrect.

        Returns:
            dict: An object containing the access token and token type.
    """
    # Authenticate the user
    user = authentication.authenticate_user(db, user.username, user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create a new access token
    access_token = authentication.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
