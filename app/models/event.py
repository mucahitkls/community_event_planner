from app.services import Base, engine
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    date_time = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    creator_id = Column(Integer, ForeignKey('users.id'))

    # Relationships
    creator = relationship("User", back_populates="events")  # Many Events are created by one User
    comments = relationship("Comment", back_populates="event",
                            cascade="all, delete-orphan")  # One Event can have many Comments

# Base.metadata.create_all(engine)
