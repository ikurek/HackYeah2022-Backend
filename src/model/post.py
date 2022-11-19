from sqlalchemy import Column, Integer, String
from src.database import Base


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    tweet_id = Column(String, unique=True)

    def __init__(self, tweet_id: str):
        self.tweet_id = tweet_id

    def __repr__(self):
        return f'<Post {self.tweet_id!r}>'
