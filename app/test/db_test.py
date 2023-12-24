# test_crud_user.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user import Base, User  # adjust the import paths according to your project structure
from app.services.crud_user import create_user, get_user, update_user, delete_user

# Configure test database
# Adjust the connection string to your test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_database.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the test tables
Base.metadata.create_all(bind=engine)


def get_test_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture
def test_db():
    # Set up the database for testing
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    # Tear down the database after the test
    db.rollback()
    db.close()


def test_create_user(test_db):
    # Use the test database session to create a user
    test_user = {"username": "testuser", "password": "testpass", "email": "test@example.com"}
    user = create_user(db=test_db, user=test_user)
    assert user.username == test_user['username']
    # Add more assertions as needed


def test_get_user(test_db):
    # Assuming you have created a user in the test setup
    user_id = 1  # adjust as necessary
    user = get_user(db=test_db, user_id=user_id)
    assert user is not None
    # Add more assertions to verify the user's details


def test_update_user(test_db):
    # Assuming you have a user to update
    user_id = 1  # adjust as necessary
    update_data = {"username": "updateduser", "password": "updatedpass", "email": "updated@example.com"}
    user = update_user(db=test_db, user_id=user_id, user=update_data)
    assert user.username == update_data['username']
    # Add more assertions as needed


def test_delete_user(test_db):
    # Assuming you have a user to delete
    user_id = 1  # adjust as necessary
    user = delete_user(db=test_db, user_id=user_id)
    assert get_user(db=test_db, user_id=user_id) is None
    # Add more assertions to verify deletion
