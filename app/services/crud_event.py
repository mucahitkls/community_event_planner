from sqlalchemy.orm import Session
from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate


def create_event(db: Session, event: EventCreate, user_id: int):
    """
        Create a new event in the database.

        Args:
            db (Session): The database session to use for the operation.
            event (EventCreate): A schema object containing the details of the event to be created.
            user_id (int): The ID of the user creating the event.

        Returns:
            Event: The newly created Event object.
    """
    db_event = Event(**event.dict(), creator_id=user_id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_event(db: Session, event_id: int):
    """
        Retrieve a single event by its ID.

        Args:
            db (Session): The database session to use for the operation.
            event_id (int): The ID of the event to retrieve.

        Returns:
            Event: The Event object if found, otherwise None.
    """
    return db.query(Event).filter(Event.id == event_id).first()


def get_events(db: Session, skip: int = 0, limit: int = 10):
    """
        Retrieve a list of events, with optional pagination.

        Args:
            db (Session): The database session to use for the operation.
            skip (int, optional): The number of items to skip before starting to collect the result set.
            limit (int, optional): The maximum number of items to return.

        Returns:
            List[Event]: A list of Event objects.
    """
    return db.query(Event).offset(skip).limit(limit).all()


def update_event(db: Session, event_id: int, event: EventUpdate):
    """
        Update the details of an existing event.

        Args:
            db (Session): The database session to use for the operation.
            event_id (int): The ID of the event to update.
            event (EventUpdate): A schema object containing the updated details of the event.

        Returns:
            Event: The updated Event object, or None if the event doesn't exist.
    """
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
    """
        Delete an event from the database.

        Args:
            db (Session): The database session to use for the operation.
            event_id (int): The ID of the event to delete.

        Returns:
            Event: The deleted Event object, or None if the event doesn't exist.
    """
    db_event = get_event(db=db, event_id=event_id)
    if db_event:
        db.delete(db_event)
        db.commit()
        return db_event
    return None
