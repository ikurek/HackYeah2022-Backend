from datetime import datetime
from src.model.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, DateTime, Boolean, Float, Integer, LargeBinary
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from typing import Optional, Any, List, Dict

import json
import struct 

class Post(Base):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tweet_id: Mapped[int] = mapped_column(Integer, unique=True)
    tweet_author_id: Mapped[str] = mapped_column(Integer)
    tweet_author_username: Mapped[str] = mapped_column(String)
    tweet_author_display_name: Mapped[str] = mapped_column(String)
    tweet_author_is_verified: Mapped[bool] = mapped_column(Boolean)
    tweet_date: Mapped[datetime] = mapped_column(DateTime)
    tweet_text: Mapped[str] = mapped_column(String)
    tweet_embeddings: Mapped[str] = mapped_column()
    tweet_like_count: Mapped[int] = mapped_column(Integer)
    tweet_reply_count: Mapped[int] = mapped_column(Integer)
    tweet_retweet_count: Mapped[int] = mapped_column(Integer)
    tweet_quote_count: Mapped[int] = mapped_column(Integer)
    tweet_language: Mapped[str] = mapped_column(String(2))
    tweet_medias_json: Mapped[str] = mapped_column(String)
    tweet_embeddings_bin: Mapped[Optional[bytes]] = mapped_column(LargeBinary, nullable=True) 
    fraud_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    social_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    def __init__(
            self,
            tweet_author_id: str,
            tweet_author_username: str,
            tweet_author_display_name: str,
            tweet_author_is_verified: bool,
            tweet_date: datetime,
            tweet_text: str,
            tweet_id: str,
            tweet_like_count: int,
            tweet_reply_count: int,
            tweet_retweet_count: int,
            tweet_quote_count: int,
            tweet_language: int,
            tweet_medias: List[Dict[str, str]],
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
        self.tweet_like_count = tweet_like_count
        self.tweet_reply_count = tweet_reply_count
        self.tweet_retweet_count = tweet_retweet_count
        self.tweet_quote_count = tweet_quote_count
        self.tweet_language = tweet_language
        self.tweet_medias_json = json.dumps(tweet_medias)

    def __repr__(self):
        return f'<Tweet ID {self.tweet_id!r}>'

    @property
    def tweet_medias(self) -> List[Dict[str, str]]:
        return json.loads(self.tweet_medias_json)

    @property 
    def tweet_embeddings(self) -> List[float]:
        emb_size = len(self.tweet_embeddings_bin) / 4
        return struct.unpack(f"<{emb_size}f", self.tweet_embeddings_bin)

    @tweet_embeddings.setter
    def tweet_embeddings(self, value):
        emb_bin = struct.pack(f"<{len(value)}f", *value)
        self.tweet_embeddings_bin = emb_bin


class PostSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        include_relationships = True
        load_instance = True
