from typing import List
from src.model.post import Post
from src.database import db_engine
from sqlalchemy import select
from sqlalchemy.orm import Session


def get_all_posts() -> List[Post]:
    with Session(db_engine) as session:
        statement = select(Post)
        result = list(session.scalars(statement))
        return result


def get_post(post_id: int) -> Post:
    with Session(db_engine) as session:
        statement = select(Post).where(Post.id == post_id)
        result = session.scalar(statement)
        return result


def insert_post(post: Post):
    with Session(db_engine) as session:
        session.add(post)
        session.commit()
        return
