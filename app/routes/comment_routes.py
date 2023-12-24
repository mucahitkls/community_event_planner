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
async def create_comment_for_event(comment: comment_schemas.CommentCreate, db: Session = Depends(database.get_db), current_user: UserInDB = Depends(authentication.get_current_user)):
    """
        Create a new comment for a specific event.

        This endpoint allows authenticated users to post comments on events.
        The user's ID is extracted from the current user context and associated with the comment.

        Args:
            comment (CommentCreate): The content of the comment to be created, along with associated event ID.
            db (Session, optional): The database session dependency.
            current_user (UserInDB, optional): The current authenticated user's information.

        Returns:
            Comment: The created Comment object as confirmation.
    """
    return crud_comment.create_comment(db=db, comment=comment, user_id=current_user.id)


@router.get("/event/{event_id}", response_model=List[comment_schemas.Comment])
async def read_comments_for_event(event_id: int, db: Session = Depends(database.get_db)):
    """
        Retrieve all comments associated with a specific event.

        This endpoint allows users to view all comments for a given event, identified by its ID.

        Args:
            event_id (int): The ID of the event for which to retrieve comments.
            db (Session, optional): The database session dependency.

        Returns:
            List[Comment]: A list of all comments associated with the specified event.
    """
    return crud_comment.get_comments_for_events(db=db, event_id=event_id)


@router.delete("/{comment_id}")
async def delete_comment(comment_id: int, db: Session = Depends(database.get_db), current_user: UserInDB = Depends(authentication.get_current_user)):
    """
        Delete a specific comment.

        This endpoint allows authenticated users to delete their own comments.
        It checks if the current user is the author of the comment before proceeding with deletion.

        Args:
            comment_id (int): The ID of the comment to be deleted.
            db (Session, optional): The database session dependency.
            current_user (UserInDB, optional): The current authenticated user's information.

        Returns:
            dict: A confirmation message indicating successful deletion.

        Raises:
            HTTPException: If the comment is not found or the user is not authorized to delete it.
    """
    success = crud_comment.delete_comment(db=db, comment_id=comment_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not fount or not authorized to delete")
    return {'message': "Comment deleted successfully"}
