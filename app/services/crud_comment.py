from sqlalchemy.orm import Session
from app.schemas.comment import CommentCreate
from app.models.comment import Comment


def create_comment(db: Session, comment: CommentCreate, user_id: int, event_id: int):
    db_comment = Comment(**comment.dict(), user_id=user_id, event_id=event_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comments_for_events(db: Session, event_id: int):
    return db.query(Comment).filter(Comment.event_id == event_id).all()


def delete_comment(db: Session, comment_id: int, user_id: int):
    comment = db.query(Comment).filter(Comment.id == comment_id, Comment.user_id == user_id).first()
    if comment:
        db.delete(comment)
        db.commit()
        return True
    return False