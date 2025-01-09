from flask import request
from flask_restx import Resource

from app.src.routes.FlaskAppSubSettings import api, logger
from app.src.utils.like_services import QueriesDatabase
from app.src.database.models import Session


@api.route("/api/tweets/<int:tweet_id>/likes")
class LikeTweetResource(Resource):
    def process_like(self, tweet_id, query_method):
        session = Session()
        db_queries = QueriesDatabase(session)

        try:
            api_key: str = request.headers.get("api-key")

            if not api_key:
                logger.error(f"DELETE Запрос на /tweets/{tweet_id}/like не обработан. Пользователь с ключом <{api_key}> не найден.")
                return {"result": False, "message": f"User with api_key{api_key} not found."}, 413

            result, status_code = db_queries.add_delete_like(api_key=api_key, tweet_id=tweet_id, query_method=query_method)

            return result, status_code

        except Exception as e:
            logger.error(f"Error in POST /api/tweets/<int:tweet_id>/likes: {e}")
            return {"result": False, "message": "Internal server error"}, 413

        finally:
            try:
                db_queries.close_session()
            except Exception as close_error:
                logger.error(f"Error closing session: {close_error}")

    @api.response(200, "Success")
    @api.doc(description="Like a tweet")
    def post(self, tweet_id):
        """ Функция-обработчик, чтобы поставить отметку <Нравиться> на твит. """
        return self.process_like(tweet_id, query_method="add")


    @api.response(200, "Success")
    @api.doc(description="Unlike a tweet")
    def delete(self, tweet_id):
        """ Функция-обработчик, для удаления отметки <Нравиться> с твита. """
        return self.process_like(tweet_id, query_method="delete")

