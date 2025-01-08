from flask import request
from flask_restx import Resource
from sqlalchemy import insert, delete

from app.src.routes.FlaskAppSubSettings import api, logger
from app.src.database.models import Session, User, ApiKey, Tweets, Like
from app.src.schemas.schemas import tweet_data_model, tweet_response_model, tweet_get_response_model
from app.src.utils.tweet_services import TweetQueriesDatabase, reformatting_data


@api.route("/api/tweets/<int:tweet_id>/likes")
class LikeTweetResource(Resource):
    @api.response(200, "Success")
    @api.doc(description="Like a tweet")
    def post(self, tweet_id):
        """ Функция-обработчик, чтобы поставить отметку <Нравиться> на твит. """
        session = Session()
        api_key: str = request.headers.get("api-key")
        user = session.query(User).join(ApiKey).filter(ApiKey.api_key == api_key).first()
        tweet = session.query(Tweets).filter(Tweets.id == tweet_id).first()

        session.execute(insert(Like).values(user_id=user.id, tweet_id=tweet_id))
        session.commit()

        # памятка: likes.py красиво оформить, БД заплнение добавить побольше данных, профиль юзера сделать

        return {"result": True}, 200

    @api.response(200, "Success")
    @api.doc(description="Unlike a tweet")
    def delete(self, tweet_id):
        """ Функция-обработчик, для удаления отметки <Нравиться> с твита. """
        session = Session()
        api_key: str = request.headers.get("api-key")
        user = session.query(User).join(ApiKey).filter(ApiKey.api_key == api_key).first()
        tweet = session.query(Tweets).filter(Tweets.id == tweet_id).first()

        session.execute(delete(Like).filter(Like.tweet_id == tweet_id, Like.user_id == user.id))
        session.commit()

        return {"result": True}, 200
