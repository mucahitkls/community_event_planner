from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import app.schemas.comment as comment_schemas
from app.schemas.user import UserInDB
from app.services import crud_comment, authentication, database
from app.models.comment import Comment



router = APIRouter(
    prefix="/comments",
    tags=["comments"],
    responses={404: {"details": "Not found"}}
)


@router.post("/", response_model=comment_schemas.Comment)
async def create_comment_for_event(event_id: int, comment: comment_schemas.CommentCreate, db: Session = Depends(database.get_db), current_user: UserInDB = Depends(authentication.get_current_user)):
    return crud_comment.create_comment(db=db, comment=comment, user_id=current_user.id, event_id=event_id)


@router.get("/event/{event_id}", response_model=List[comment_schemas.Comment])
async def read_comments_for_event(event_id: int, db: Session = Depends(database.get_db)):
    return crud_comment.get_comments_for_events(db=db, event_id=event_id)


@router.delete("/{comment_id}", status_code=204)
async def delete_comment(comment_id: int, db: Session = Depends(database.get_db), current_user: UserInDB = Depends(authentication.get_current_user)):
    success = crud_comment.delete_comment(db=db, comment_id=comment_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not fount or not authorized to delete")
    return {'message': "Comment deleted successfully"}
