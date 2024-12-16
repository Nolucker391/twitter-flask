from sqlalchemy import (Column, Integer, String, ForeignKey,
                        Table, create_engine, MetaData)
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

from app.src.settings.config import (DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
metadata = MetaData()
Session = sessionmaker(bind=engine)
Base = declarative_base()

followers = Table(
    "followers",
    Base.metadata,
    Column("follower_id", Integer, ForeignKey("users.id")),
    Column("following_id", Integer, ForeignKey("users.id")),
)

likes = Table(
    "likes",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("tweet_id", Integer, ForeignKey("tweets.id")),
)

tweet_media_association = Table(
    "tweet_media_association",
    Base.metadata,
    Column("tweet_id", Integer, ForeignKey("tweets.id")),
    Column("media_id", Integer, ForeignKey("media.id")),
)

class Media(Base):
    __tablename__ = "media"
    id = Column(Integer, primary_key=True)
    file_src = Column(String)
    file_name = Column(String)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    api_key = Column(String(), nullable=True)
    authored_tweets = relationship(
        "Tweet", backref="author", foreign_keys="Tweet.author_id"
    )

    followers = relationship(
        "User",
        secondary=followers,
        primaryjoin=(followers.c.following_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        backref="following",
    )

class Tweet(Base):
    __tablename__ = "tweets"
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"))
    media = relationship("Media", secondary=tweet_media_association, backref="tweets")
    liked_by_users = relationship("User", secondary=likes, backref="liked_tweets")
