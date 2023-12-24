from sqlalchemy.orm import Session
from app.schemas.comment import CommentCreate
from app.models.comment import Comment


def create_comment(db: Session, comment: CommentCreate, user_id: int):
    """
        Create a new comment in the database.

        Args:
            db (Session): The database session to use for the operation.
            comment (CommentCreate): A CommentCreate schema object containing the content of the comment.
            user_id (int): The ID of the user who is creating the comment.

        Returns:
            Comment: The newly created Comment object.
    """

    db_comment = Comment(**comment.dict(), user_id=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comments_for_events(db: Session, event_id: int):
    """
        Retrieve all comments associated with a specific event from the database.

        Args:
            db (Session): The database session to use for the operation.
            event_id (int): The ID of the event for which to retrieve comments.

        Returns:
            List[Comment]: A list of Comment objects associated with the specified event.
    """
    return db.query(Comment).filter(Comment.event_id == event_id).all()


def delete_comment(db: Session, comment_id: int, user_id: int):
    """
        Delete a comment from the database if the user is the author.

        Args:
            db (Session): The database session to use for the operation.
            comment_id (int): The ID of the comment to be deleted.
            user_id (int): The ID of the user attempting to delete the comment.

        Returns:
            bool: True if the comment was successfully deleted, False otherwise.
    """
    comment = db.query(Comment).filter(Comment.id == comment_id, Comment.user_id == user_id).first()
    if comment:
        db.delete(comment)
        db.commit()
        return True
    return False