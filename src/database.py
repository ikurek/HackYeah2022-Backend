from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.model.base import Base

db_engine = create_engine('sqlite:///local.db?charset=utf8', echo=True, future=True)


def init_db():
    print("DB init")
    import src.model.post
    Base.metadata.create_all(db_engine)
