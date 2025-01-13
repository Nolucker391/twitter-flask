from flask import jsonify
import logging
# from app.src.routes.FlaskAppSubSettings import logger
from sqlalchemy import delete, insert, select
from app.src.database.models import ApiKey, User, user_following

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def formatted_data_user(query):
    response_data = {
        "result": True,
        "user": {
            "id": query.id,
            "name": query.name,
            "followers": [
                {
                    "id": f.id,
                    "name": f.name
                }
                for f in query.followers
            ],
            "following": [
                {
                    "id": f.id,
                    "name": f.name
                }
                for f in query.following
            ]
        }
    }

    return response_data

class QueriesDatabase:
    def __init__(self, session):
        """Инициализация сессии базы данных."""
        self.session = session

    def get_user_profile(self, user_id):
        """Функция, для отображения профиля пользователя."""
        query = self.session.query(User).filter_by(id=user_id).first()

        try:
            if not query:
                return jsonify({"error": "Пользователь с таким ID не найден."}), 401

            return formatted_data_user(query)

        except Exception as e:
            logger.error(f"Error in POST /api/users/<int:{user_id}>: {e}")
            return {"result": False, "message": "Internal server error"}, 413

    def get_user_with_api(self, api_key):
        """Функция, для отображения информации о пользователе."""
        query = self.session.query(User).join(ApiKey).filter(ApiKey.api_key == api_key).first()

        try:
            if not query:
                return {"error": "Пользователь с таким API не найден."}, 401

            return formatted_data_user(query)

        except Exception as e:
            logger.error(f"Error in POST /api/users/<int:{query.id}>: {e}")
            return {"result": False, "message": "Internal server error"}, 413

    def follow_processing_users(self, api_key, following_id):
        """Функция, для подписки и отписки на профиль пользователя."""
        user = self.session.query(User).join(ApiKey).filter(ApiKey.api_key == api_key).first()

        try:
            select_user_query = select(User).where(User.id == following_id)
            user_to_follow = self.session.execute(select_user_query)
            user_to_follow = user_to_follow.scalar_one_or_none()

            if user_to_follow:
                exist_follow = self.session.execute(
                    select(user_following).filter(
                        user_following.c.user_id == user.id,
                        user_following.c.following_id == following_id,
                    )
                )
                exist_follow = exist_follow.scalars().one_or_none()

                if exist_follow:
                    stmt = delete(user_following).filter(
                        user_following.c.user_id == user.id,
                        user_following.c.following_id == following_id,
                    )
                    self.session.execute(stmt)
                    self.session.commit()

                    return {"result": True}
                    # return {
                    #     "result": False,
                    #     "error_message": f"Пользователь с id={user.id} уже подписан на пользователя с id={following_id}",
                    #     "error_type": "FollowExist",
                    # }
                else:
                    stmt = insert(user_following).values(user_id=user.id, following_id=following_id)
                    self.session.execute(stmt)
                    self.session.commit()

                    return {"result": True}

        except Exception as e:
            logger.error(f"Error in POST /api/users/<int:{following_id}>: {e}")
            return {"result": False, "message": "Internal server error"}, 413

    def close_session(self):
        """Закрыть сессию после завершения работы."""
        self.session.close()
