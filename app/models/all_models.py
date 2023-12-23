from app.services import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)

    # Relationships
    events = relationship("Event", back_populates="creator")
    comments = relationship("Comment", back_populates="author")


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    date_time = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    creator_id = Column(Integer, ForeignKey('users.id'))

    # Relationships
    creator = relationship("User", back_populates="events")
    comments = relationship("Comment", back_populates="events")


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    event_id = Column(Integer, ForeignKey('events.id'))

    # Relationships
    author = relationship("User", back_populates="comments")
    event = relationship("Event", back_populates="comments")
