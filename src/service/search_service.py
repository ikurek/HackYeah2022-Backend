from typing import List
from src.model.post import Post
from src.database import db_engine
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from src.service.post_service import get_all_posts
from datetime import datetime


def find_posts(
        smart_search_query: str,
        keyword: str,
        author_username: str,
        from_date: datetime,
        to_date: datetime
) -> List[Post]:
    print(
        f'Search params: \n    query: {smart_search_query}\n    keyword: {keyword}\n    username: {author_username}\n '
        f'   from_date: {from_date.isoformat()}\n    to_date: {to_date.isoformat()}')
    if len(smart_search_query) > 0:
        return get_posts_with_smart_search(smart_search_query, from_date, to_date)
    elif len(keyword) > 0:
        return get_posts_with_keyword(keyword, from_date, to_date)
    elif len(author_username) > 0:
        return get_posts_with_author_username(author_username, from_date, to_date)
    else:
        return get_all_posts(from_date, to_date)


def get_posts_with_keyword(keyword: str, from_date: datetime, to_date: datetime) -> List[Post]:
    with Session(db_engine) as session:
        print(f'Searching by keyword')
        statement = select(Post).filter(Post.tweet_date.between(from_date, to_date)).filter(
            func.lower(Post.tweet_text).contains(keyword.lower()))
        return list(session.scalars(statement))


def get_posts_with_smart_search(smart_search_query: str, from_date: datetime, to_date: datetime) -> List[Post]:
    with Session(db_engine) as session:
        print(f'Searching by smart search')
        # TODO: KAMIL
        return list()


def get_posts_with_author_username(author_username: str, from_date: datetime, to_date: datetime) -> List[Post]:
    with Session(db_engine) as session:
        print(f'Searching by username')
        statement = select(Post).filter(Post.tweet_date.between(from_date, to_date)).filter(
            func.lower(Post.tweet_author_username) == author_username.lower())
        return list(session.scalars(statement))
