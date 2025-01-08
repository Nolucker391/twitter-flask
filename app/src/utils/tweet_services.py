from sqlalchemy import insert, select, update, delete

from app.src.routes.FlaskAppSubSettings import logger
from app.src.database.models import User, ApiKey, Tweets, Image


def reformatting_data(tweets):
    """ Функция, для правильного вывода формата данных о твитах. """
    response_data = {
        "result": True,
        "tweets": [
            {
                "id": tweet.id,
                "content": tweet.content,
                "attachments": [
                    f"static/medias/user_api_{key.api_key}/{link.filename}"
                    for key in tweet.author.api_key
                    for link in tweet.attachments
                ],
                "author": {
                    "id": tweet.author_id,
                    "name": tweet.author.name
                },
                "likes": [
                    {
                        "user_id": like.user_like.id,
                        "name": like.user_like.name
                    }
                    for like in tweet.likes_by_users
                ],
            }
            for tweet in tweets
        ],
    }

    return response_data

class TweetQueriesDatabase:
    def __init__(self, session):
        """ Инициализация сессии базы данных. """
        self.session = session

    def get_tweets(self):
        """ Получение всех твитов с БД. """
        query_tweets = self.session.execute(select(Tweets)).scalars().all()

        return query_tweets

    def add_tweet(self, api_key, tweet_data):
        """ Добавление твита в БД. """
        try:
            query = self.session.query(User).join(ApiKey).filter(ApiKey.api_key == api_key).first()
            query2 = self.session.execute(insert(Tweets).values(author_id=query.id, content=tweet_data.get("tweet_data")).returning(Tweets.id))

            self.session.commit()

            tweet_id = query2.scalar_one_or_none()

            media_ids = tweet_data.get("tweet_media_ids")

            if media_ids:
                for m_id in media_ids:
                    self.session.execute(update(Image).where(Image.id == m_id).values(tweet_id=tweet_id))
                    self.session.commit()

            return tweet_id

        except Exception as e:
            logger.error(f"Error add tweet from database: {e}")

    def delete_tweet(self, api_key, tweet_id):
        """ Удаление твита в БД. """
        try:
            user = self.session.query(User).join(ApiKey).filter(ApiKey.api_key == api_key).first()
            tweet = self.session.query(Tweets).filter(Tweets.id == tweet_id).first()

            if not tweet:
                logger.info(f"Твит с id({tweet_id}) не найден.")
                return {"result": False, "message": f"Tweet with id({tweet_id}) not found."}, 413

            if tweet.author_id != user.id:
                logger.info(f"Пользователь id({user.id}) - не является автором твита.")
                return {"result": False, "message": f"User id({user.id}) is not the author of the tweet."}, 403

            tweet_del = delete(Tweets).where(Tweets.id == tweet_id)
            self.session.execute(tweet_del)
            self.session.commit()

            return {"result": True}, 200

        except Exception as e:
            logger.error(f"Error delete tweet from database: {e}")

    def close_session(self):
        """Закрыть сессию после завершения работы."""
        self.session.close()