from ..database import db_engine
from ..model.post import Post
from ..model.influencer import Influencer
from ..service.post_service import get_all_posts
from ..ml.language import polish_text_to_embeddings

from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from typing import List
import numpy as np


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


def get_author_ranking(from_date: datetime, to_date: datetime) -> List[Influencer]:
    with Session(db_engine) as session:
        statement = select(Post).filter(Post.tweet_date.between(from_date, to_date))
        result = list(session.scalars(statement))

        authors = {}
        authors_social_sums = {}
        authors_fraud_sums = {}
        authors_counts = {}
        for post in result:
            author_id = post.tweet_author_id
            if author_id not in authors:
                authors[author_id] = Influencer(post.tweet_author_id, post.tweet_author_username, post.tweet_author_display_name, 0.0, 0.0)
            if author_id in authors_social_sums:
                authors_social_sums[author_id] += post.social_score or 0.0
            else:
                authors_social_sums[author_id] = post.social_score or 0.0
            if author_id in authors_fraud_sums:
                authors_fraud_sums[author_id] += post.fraud_score or 0.0
            else:
                authors_fraud_sums[author_id] = post.fraud_score or 0.0
            if author_id in authors_counts:
                authors_counts[author_id] += 1
            else:
                authors_counts[author_id] = 1
        
        for id, author in authors.items():
            author.social_score = authors_social_sums[id] / authors_counts[id]
            author.fraud_score = authors_fraud_sums[id] / authors_counts[id]
        
        sorted_authors = sorted(authors.values(), key=lambda a: a.social_score, reverse=True)

        return sorted_authors


def get_posts_with_keyword(keyword: str, from_date: datetime, to_date: datetime) -> List[Post]:
    with Session(db_engine) as session:
        print(f'Searching by keyword')
        statement = select(Post).filter(Post.tweet_date.between(from_date, to_date)).filter(
            func.lower(Post.tweet_text).contains(keyword.lower()))
        return list(session.scalars(statement))


def get_posts_with_smart_search(smart_search_query: str, from_date: datetime, to_date: datetime) -> List[Post]:
    with Session(db_engine) as session:
        posts = get_all_posts(from_date, to_date)
        smart_search_embeddings = np.array([polish_text_to_embeddings(smart_search_query)])
        embeddings = np.array([post.tweet_embeddings for post in posts])
        similarities = cosine_similarity(smart_search_embeddings, embeddings)
        posts_with_similarities = zip(posts, similarities[0])
        sorted_posts_with_similarities = sorted(posts_with_similarities, key=lambda tup: tup[1])
        return [post[0] for post in sorted_posts_with_similarities]


def get_posts_with_author_username(author_username: str, from_date: datetime, to_date: datetime) -> List[Post]:
    with Session(db_engine) as session:
        print(f'Searching by username')
        statement = select(Post).filter(Post.tweet_date.between(from_date, to_date)).filter(
            func.lower(Post.tweet_author_username) == author_username.lower())
        return list(session.scalars(statement))
