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
    return crud_event.create_event(db=db, event=event, user_id=current_user.id)


@router.get("/", response_model=List[event_schemas.Event])
async def read_events(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    events = crud_event.get_events(db=db, skip=skip, limit=limit)
    return events


@router.get("/{event_id}", response_model=event_schemas.Event)
async def read_event(event_id: int, db: Session = Depends(get_db)):
    db_event = crud_event.get_event(db=db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@router.put("/{event_id}", response_model=event_schemas.Event)
async def update_event(event_id: int, event: event_schemas.EventUpdate, db: Session = Depends(get_db),
                       current_user: UserInDB = Depends(authentication.get_current_user)):
    db_event = crud_event.get_event(db=db, event_id=event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    if db_event.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this event")
    return crud_event.update_event(db=db, event_id=event_id, event=event)


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(event_id: int, db: Session = Depends(get_db),
                       current_user: UserInDB = Depends(authentication.get_current_user)):
    db_event = crud_event.get_event(db=db, event_id=event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    if db_event.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this event")
    return crud_event.delete_event(db, event_id=event_id)
