from app.src.database.models import ApiKey, Like, Tweets, User
from app.src.routes.FlaskAppSubSettings import logger
from sqlalchemy import delete, insert


class QueriesDatabase:
    def __init__(self, session):
        """Инициализация сессии базы данных."""
        self.session = session

    def add_delete_like(self, api_key, tweet_id, query_method):
        """Функция, для добавления и удаления отметки <Нравиться>."""
        user = (
            self.session.query(User)
            .join(ApiKey)
            .filter(ApiKey.api_key == api_key)
            .first()
        )
        tweet = self.session.query(Tweets).filter(Tweets.id == tweet_id).first()

        if not tweet:
            logger.info(f"Твит с id({tweet_id}) не найден.")
            return {
                "result": False,
                "message": f"Tweet with id({tweet_id}) not found.",
            }, 413
        try:
            if query_method == "add":
                self.session.execute(
                    insert(Like).values(user_id=user.id, tweet_id=tweet_id)
                )
            elif query_method == "delete":
                self.session.execute(
                    delete(Like).filter(
                        Like.tweet_id == tweet_id, Like.user_id == user.id
                    )
                )
            else:
                logger.info(f"Метод запроса не опеределен или неверен {query_method}.")
                return {"result": False, "message": f"Internal server error."}, 413

            self.session.commit()
            return {"result": True}, 200

        except Exception as e:
            logger.error(f"Error in POST /api/tweets/<int:tweet_id>/likes: {e}")
            return {"result": False, "message": "Internal server error"}, 413

    def close_session(self):
        """Закрыть сессию после завершения работы."""
        self.session.close()
