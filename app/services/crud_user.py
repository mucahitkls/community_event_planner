from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext
from app.models.user import User
from app.schemas.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_username(db: Session, username: str):
    """
        Retrieve a user by their username.

        Args:
            db (Session): The database session to use for the operation.
            username (str): The username of the user to retrieve.

        Returns:
            User: The User object if found, otherwise None.
    """
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    """
        Retrieve a user by their email.

        Args:
            db (Session): The database session to use for the operation.
            email (str): The email of the user to retrieve.

        Returns:
            User: The User object if found, otherwise None.
    """
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    """
        Create a new user in the database.

        Args:
            db (Session): The database session to use for the operation.
            user (UserCreate): A schema object containing the details of the user to be created.

        Returns:
            User: The newly created User object.

        Raises:
            SQLAlchemyError: If there is an issue committing to the database.
    """
    hashed_password_ = pwd_context.hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password_)
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        raise e


def get_user(db: Session, user_id: int):
    """
        Retrieve a user by their user ID.

        Args:
            db (Session): The database session to use for the operation.
            user_id (int): The ID of the user to retrieve.

        Returns:
            User: The User object if found, otherwise None.
    """
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    """
        Retrieve a list of users, with optional pagination.

        Args:
            db (Session): The database session to use for the operation.
            skip (int, optional): The number of items to skip before starting to collect the result set.
            limit (int, optional): The maximum number of items to return.

        Returns:
            List[User]: A list of User objects.
    """
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, user: UserCreate):
    """
        Update the details of an existing user.

        Args:
            db (Session): The database session to use for the operation.
            user_id (int): The ID of the user to update.
            user (UserCreate): A schema object containing the updated details of the user.

        Returns:
            User: The updated User object, or None if the user doesn't exist.
    """
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    for var, value in vars(user).items():
        setattr(db_user, var, value) if value else None

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    """
        Delete a user from the database.

        Args:
            db (Session): The database session to use for the operation.
            user_id (int): The ID of the user to delete.

        Returns:
            User: The deleted User object, or None if the user doesn't exist.
    """
    db_user = get_user(db, user_id)
    if not db_user:
        return None

    db.delete(db_user)
    db.commit()
    return db_user
