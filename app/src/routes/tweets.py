from app.src.database.models import Session
from app.src.routes.FlaskAppSubSettings import api, logger
from app.src.schemas.schemas import (
    tweet_data_model,
    tweet_get_response_model,
    tweet_response_model,
)
from app.src.utils.tweet_services import TweetQueriesDatabase, reformatting_data
from flask import request
from flask_restx import Resource


@api.route("/api/tweets")
class TweetResource(Resource):
    @api.expect(tweet_data_model, validate=True)
    @api.response(200, "Success", tweet_response_model)
    @api.doc(description="Create a new tweet")
    def post(self):
        """Функция-обработчик, для создания нового твита."""
        session = Session()
        db_queries = TweetQueriesDatabase(session)

        try:
            tweet_data = request.json
            api_key = request.headers.get("api-key")

            tweet_id = db_queries.add_tweet(api_key=api_key, tweet_data=tweet_data)

            return {"result": True, "tweet_id": tweet_id}, 200

        except Exception as e:
            logger.error(f"Error in POST /api/tweets: {e}")
            return {"result": False, "message": "Internal server error"}, 413

        finally:
            try:
                db_queries.close_session()
            except Exception as close_error:
                logger.error(f"Error closing session: {close_error}")

    @api.response(200, "Success", tweet_get_response_model)
    @api.doc(description="Show all tweets.")
    def get(self):
        """Функция-обработчик, для отображения всех твитов на странице."""
        session = Session()
        db_queries = TweetQueriesDatabase(session)

        try:
            tweets = db_queries.get_tweets()

            response_data = reformatting_data(tweets)

            return response_data, 200

        except Exception as e:
            logger.error(f"Error in GET /api/tweets: {e}")
            return {"result": False, "message": "Internal server error"}, 500

        finally:
            try:
                db_queries.close_session()
            except Exception as close_error:
                logger.error(f"Error closing session: {close_error}")


@api.route("/api/tweets/<int:tweet_id>")
class TweetIdResource(Resource):
    @api.response(200, "Success")
    @api.doc(description="Delete a tweet")
    def delete(self, tweet_id):
        """Функция-обработчик, для удаления твита."""
        session = Session()
        db_queries = TweetQueriesDatabase(session)

        try:
            api_key = request.headers.get("api-key")

            if not api_key:
                logger.error(
                    f"DELETE Запрос на /tweets{tweet_id} не обработан. Пользователь с ключом <{api_key}> не найден."
                )
                return {
                    "result": False,
                    "message": f"User with api_key{api_key} not found.",
                }, 413

            result, status_code = db_queries.delete_tweet(
                api_key=api_key, tweet_id=tweet_id
            )

            return result, status_code

        except Exception as e:
            logger.error(
                f"DELETE запрос на /tweets/{id}. Детали: {str(e.__dict__['orig'])}"
            )
            return {"result": False}, 413

        finally:
            try:
                db_queries.close_session()
            except Exception as close_error:
                logger.error(f"Error closing session: {close_error}")
