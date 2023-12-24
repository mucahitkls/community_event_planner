"""
This script sets up the database connection and session management for the application.
It utilizes SQLAlchemy for ORM and database interaction, leveraging environment variables to manage configuration securely.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(url=DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

Base.metadata.create_all(engine)


def get_db():
    """
        Dependency that provides a SQLAlchemy session and ensures it's closed after use.

        This is a generator that yields a database session and closes it after the request is processed.
        It's typically used as a dependency in route handlers to provide a session for database operations.

        Yields:
            Session: The SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
