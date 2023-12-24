from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext
from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate


def create_event(db: Session, event: EventCreate, user_id: int):
    db_event = Event(**event.dict(), creator_id=user_id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_event(db: Session, event_id: int):
    return db.query(Event).filter(Event.id == event_id).first()


def get_events(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Event).offset(skip).limit(limit).all()


def update_event(db: Session, event_id: int, event: EventUpdate):
    db_event = get_event(db=db, event_id=event_id)
    if db_event:
        update_data = event.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_event, key, value)
        db.commit()
        db.refresh(db_event)
        return db_event
    return None


def delete_event(db: Session, event_id: int):
    db_event = get_event(db=db, event_id=event_id)
    if db_event:
        db.delete(db_event)
        db.commit()
        return db_event
    return None
