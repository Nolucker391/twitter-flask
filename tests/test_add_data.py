import pytest

from app.src.database.models import User, Tweets, ApiKey, Like, Image
from tests.conftest import data


@pytest.fixture(scope="function")
def test_user_data(db_session):
    """Тест для создания пользователя в БД."""
    user = User(name=data.get("names")[0])
    db_session.add(user)
    db_session.commit()

    api_key = ApiKey(user_id=user.id, api_key=data.get("api-keys")[0])
    user.api_key.append(api_key)
    db_session.commit()

    return user

@pytest.fixture(scope="function")
def test_tweet_data(db_session, test_user_data):
    """Тест для создания твита в БД."""

    tweet_content = Tweets(author_id=test_user_data.id, content=data.get("content")[0])
    db_session.add(tweet_content)
    db_session.commit()

    return tweet_content

@pytest.fixture(scope="function")
def test_tweet_attachments(db_session, test_tweet_data, test_user_data):
    """Тест для добавления всех вложений."""

    tweet_likes = Like(user_id=test_user_data.id, tweet_id=test_tweet_data.id)
    media_tweet = Image(filename=data.get("filename")[0], tweet_id=test_tweet_data.id)

    test_tweet_data.likes_by_users.append(tweet_likes)
    test_tweet_data.attachments.append(media_tweet)
    db_session.commit()


def test_all_parameters_on_database(db_session, test_tweet_data, test_user_data, test_tweet_attachments):
    tweet = db_session.query(Tweets).filter_by(author_id=test_user_data.id).first()

    assert tweet is not None
    assert tweet.author.name == data.get("names")[0]
    assert tweet.content == data.get("content")[0]
    assert tweet.author_id == test_user_data.id

    for likes in tweet.likes_by_users:
        assert likes.user_id == test_user_data.id
        assert likes.tweet_id == test_tweet_data.id

    for media in tweet.attachments:
        assert media.filename == data.get("filename")[0]
        assert media.tweet_id == test_tweet_data.id
