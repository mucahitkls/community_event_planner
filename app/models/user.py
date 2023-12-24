from app.services import Base, engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    #email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)

    # Relationships
    events = relationship("Event", back_populates="creator")
    comments = relationship("Comment", back_populates="author")


Base.metadata.create_all(engine)
