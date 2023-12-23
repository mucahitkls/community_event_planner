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
    Create a new user with provided username and password
    :param user:
    :param db:
    :return:
    """
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db=db, user=user)


@router.get("/", response_model=List[user_schema.User])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve a list of users.
    :param skip:
    :param limit:
    :param db:
    :return:
    """
    users = crud_user.get_users()
    return users


@router.get("/{user_id}", response_model=user_schema.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific user by id.
    :param user_id:
    :param db:
    :return:
    """
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{user_id}", response_model=user_schema.User)
async def update_user(user_id: int, user: user_schema.UserCreate, db: Session = Depends(get_db)):
    """
    Update a user
    :param user_id:
    :param user:
    :param db:
    :return:
    """

    return crud_user.update_user(db=db, user_id=user_id, user=user)


@router.delete("/{user_id}", response_model=user_schema.User)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Deletes a user
    :param user_id:
    :param db:
    :return:
    """
    return crud_user.delete_user(db=db, user_id=user_id)

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
       OAuth2 compatible token login, get an access token for future requests.
    """

    # Authenticate the user
    user = authentication.authenticate_user(db, form_data.username, form_data.password, form_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Create a new access token
    access_token = authentication.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}



