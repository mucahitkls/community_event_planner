from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.schemas import event as event_schemas
from app.schemas.user import UserInDB
from app.services import crud_event
from app.services.database import get_db
import app.services.authentication as authentication

router = APIRouter(
    prefix='/events',
    tags=["events"],
    responses={404: {"description": "Not found"}}
)


@router.post("/", response_model=event_schemas.Event)
async def create_event(event: event_schemas.EventCreate, db: Session = Depends(get_db),
                       current_user: UserInDB = Depends(authentication.get_current_user)):
    """
        Create a new event.

        Allows an authenticated user to create a new event with the provided details.
        The user's ID is extracted from the current user context and associated with the event as the creator.

        Args:
            event (EventCreate): The details of the event to be created.
            db (Session, optional): The database session dependency.
            current_user (UserInDB, optional): The current authenticated user's information.

        Returns:
            Event: The created Event object with details.
    """
    return crud_event.create_event(db=db, event=event, user_id=current_user.id)


@router.get("/", response_model=List[event_schemas.Event])
async def read_events(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
        Retrieve a list of events, with optional pagination.

        Provides a list of all available events, supporting pagination via skip and limit parameters.

        Args:
            skip (int, optional): The number of items to skip before starting to collect the result set.
            limit (int, optional): The maximum number of items to return.
            db (Session, optional): The database session dependency.

        Returns:
            List[Event]: A list of Event objects.
    """
    events = crud_event.get_events(db=db, skip=skip, limit=limit)
    return events


@router.get("/{event_id}", response_model=event_schemas.Event)
async def read_event(event_id: int, db: Session = Depends(get_db)):
    """
        Retrieve a single event by its ID.

        Provides the details of a specific event, identified by its unique ID.

        Args:
            event_id (int): The unique identifier of the event to retrieve.
            db (Session, optional): The database session dependency.

        Raises:
            HTTPException: 404 error if the event is not found.

        Returns:
            Event: The Event object with details if found.
    """
    db_event = crud_event.get_event(db=db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@router.put("/{event_id}", response_model=event_schemas.Event)
async def update_event(event_id: int, event: event_schemas.EventUpdate, db: Session = Depends(get_db),
                       current_user: UserInDB = Depends(authentication.get_current_user)):
    """
       Update the details of an existing event.

       Allows the creator of the event to update its details. Checks for user authorization before proceeding.

       Args:
           event_id (int): The ID of the event to update.
           event (EventUpdate): The updated details of the event.
           db (Session, optional): The database session dependency.
           current_user (UserInDB, optional): The current authenticated user's information.

       Raises:
           HTTPException: 404 error if the event is not found or 403 if the user is not authorized to update it.

       Returns:
           Event: The updated Event object with new details.
    """
    db_event = crud_event.get_event(db=db, event_id=event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    if db_event.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this event")
    return crud_event.update_event(db=db, event_id=event_id, event=event)


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(event_id: int, db: Session = Depends(get_db),
                       current_user: UserInDB = Depends(authentication.get_current_user)):
    """
        Delete an event.

        Allows the creator of the event to delete it. Checks for user authorization before proceeding.

        Args:
            event_id (int): The ID of the event to delete.
            db (Session, optional): The database session dependency.
            current_user (UserInDB, optional): The current authenticated user's information.

        Raises:
            HTTPException: 404 error if the event is not found or 403 if the user is not authorized to delete it.

        Returns:
            dict: A confirmation message indicating successful deletion.
    """
    db_event = crud_event.get_event(db=db, event_id=event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    if db_event.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this event")
    return crud_event.delete_event(db, event_id=event_id)
