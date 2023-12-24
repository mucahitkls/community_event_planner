from app.services import Base, engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    event_id = Column(Integer, ForeignKey('events.id'))

    # Relationships
    author = relationship("User", back_populates="comments")
    events = relationship("Event", back_populates="comments")

Base.metadata.create_all(engine)