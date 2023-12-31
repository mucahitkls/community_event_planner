from app.services.database import *
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import logging

# Configuring logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def test_db_connection():
    # Only create tables if in a development environment
    Base.metadata.create_all(engine)  # Assuming dev environment
    try:
        session = SessionLocal()
        result = session.execute(text("Select version();"))
        for row in result:
            logging.info(f"Database connection success: {row[0]}")
    except SQLAlchemyError as e:
        logging.error(f"Database error occurred: {e}")
    except Exception as e:
        logging.exception(f"An unexpdected error occurred: {e}")
    finally:
        if 'session' in locals():
            session.close()


if __name__ == "__main__":
    logging.info("Starting database connection test...")
    test_db_connection()
    logging.info("Database connection test completed.")
