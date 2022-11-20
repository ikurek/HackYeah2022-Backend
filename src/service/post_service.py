from typing import List
from src.model.post import Post
from src.database import db_engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime

from typing import List, Optional

def get_all_posts(from_date: datetime, to_date: datetime) -> List[Post]:
    with Session(db_engine) as session:
        statement = select(Post).filter(Post.tweet_date.between(from_date, to_date))
        result = list(session.scalars(statement))
        return result


def get_post(post_id: int) -> Post:
    with Session(db_engine) as session:
        statement = select(Post).where(Post.id == post_id)
        result = session.scalar(statement)
        return result


def get_latest_post(lang: str) -> Optional[Post]:
    with Session(db_engine) as session:
        statement = select(Post).where(Post.tweet_language == lang).order_by(Post.tweet_date.desc()).limit(1)
        result = session.scalar(statement)
        return result


def insert_post(post: Post):
    with Session(db_engine) as session:
        session.add(post)
        session.commit()


def insert_posts(posts: List[Post]):
    with Session(db_engine) as session:
        session.add_all(posts)
        session.commit()
