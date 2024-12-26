from sqlalchemy import (Column, Integer, String, ForeignKey,
                        Table, UniqueConstraint)
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

from app.src.settings.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)  # создаем движок для SQLAlchemyORM, для подключение к БД POSTGRES
metadata = MetaData()  # экземпляр для работы с метаданными БД
Session = sessionmaker(bind=engine)  # создаем сессию(подключение) к БД
Base = declarative_base()


class User(Base):
    """ Модель, описывающий информацию о пользователе. """
    __tablename__ = "users" # имя таблицы в бд

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    tweets = relationship("Tweets", back_populates="author")
    likes_for_tweets = relationship("Like", back_populates="user_like", lazy="select")
    following = relationship(
        "User",
        secondary="user_following",
        primaryjoin="User.id==user_following.c.user_id",
        secondaryjoin="User.id==user_following.c.following_id",
        cascade="all",
        lazy="selectin",
    )
    followers = relationship(
        "User",
        secondary="user_following",
        primaryjoin="User.id==user_following.c.following_id",
        secondaryjoin="User.id==user_following.c.user_id",
        cascade="all",
        lazy="selectin",
    )


user_following = Table(
    "user_following",
    Base.metadata,
    Column("user_id", Integer, ForeignKey(User.id), primary_key=True),
    Column("following_id", Integer, ForeignKey(User.id), primary_key=True),
    UniqueConstraint("following_id", "user_id", name="unique_following"),
)


class ApiKey(Base):
    """Модель, описывающий ключ для аунтефикации пользователя."""
    __tablename__ = "keys"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    api_key = Column(String, nullable=False, unique=True)


class Tweets(Base):
    """ Модель опубликованных Твитов. """
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    content = Column(String, nullable=False)
    attachments = relationship(
        "Image", back_populates="tweet", cascade="all", lazy="selectin"
    ) # cascade=all - при удалении, удаляют за собой все вложения, которые присутствуют
    likes_by_users = relationship(
        "Like", back_populates="tweet_like", lazy="select", cascade="all"
    )
    author = relationship(
        "User", back_populates="tweets", lazy="selectin", cascade="all"
    )


class Like(Base):
    """Модель, описывающий лайки на посты от пользователей."""
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    tweet_id = Column(Integer, ForeignKey("tweets.id", ondelete="CASCADE"))
    user_like = relationship("User", back_populates="likes_for_tweets", lazy="selectin")
    tweet_like = relationship("Tweets", back_populates="likes_by_users", lazy="selectin")

    __table_args__ = (UniqueConstraint("user_id", "tweet_id", name="user_tweet_uc"),)


class Image(Base):
    """Модель изображений на твиты."""
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(100), nullable=False)
    tweet_id = Column(
        Integer, ForeignKey("tweets.id", ondelete="CASCADE"), nullable=True
    )
    tweet = relationship("Tweets", back_populates="attachments")


