from datetime import datetime
from src.model.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, DateTime, Boolean, Float
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from typing import Optional, Any


class Post(Base):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tweet_id: Mapped[str] = mapped_column(String, unique=True)
    tweet_author_id: Mapped[str] = mapped_column(String(64))
    tweet_author_username: Mapped[str] = mapped_column(String(255))
    tweet_author_display_name: Mapped[str] = mapped_column(String(255))
    tweet_author_is_verified: Mapped[bool] = mapped_column(Boolean)
    tweet_date: Mapped[datetime] = mapped_column(DateTime)
    tweet_text: Mapped[str] = mapped_column(String(140))
    fraud_score: Mapped[Optional[float]]
    social_score: Mapped[Optional[float]]

    def __init__(
            self,
            tweet_author_id: str,
            tweet_author_username: str,
            tweet_author_display_name: str,
            tweet_author_is_verified: bool,
            tweet_date: datetime,
            tweet_text: str,
            tweet_id: str,
            **kw: Any
    ):
        super().__init__(**kw)
        self.tweet_id = tweet_id
        self.tweet_author_id = tweet_author_id
        self.tweet_author_username = tweet_author_username
        self.tweet_author_display_name = tweet_author_display_name
        self.tweet_author_is_verified = tweet_author_is_verified
        self.tweet_date = tweet_date
        self.tweet_text = tweet_text

    def __repr__(self):
        return f'<Tweet ID {self.tweet_id!r}>'


class PostSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        include_relationships = True
        load_instance = True
