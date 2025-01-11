from flask import request, jsonify
from flask_restx import Resource

from app.src.routes.FlaskAppSubSettings import api, logger
from app.src.database.models import Session
from app.src.schemas.schemas import user_detail

from app.src.utils.user_services import QueriesDatabase


@api.route("/api/users/me")
class CurrentUserResource(Resource):
    @api.response(200, "Success", user_detail)
    @api.doc(description="Get current user's profile")
    def get(self):
        """
        Метод для выдачи информации о пользователе на главной странице.
        """
        session = Session()
        db_queries = QueriesDatabase(session)

        try:
            api_key = request.headers.get("Api-Key")

            query = db_queries.get_user_with_api(api_key=api_key)

            if query:
                return query, 200

        except Exception as e:
            return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

        finally:
            try:
                db_queries.close_session()
            except Exception as close_error:
                logger.error(f"Error closing session: {close_error}")


@api.route("/api/users/<int:user_id>")
class UserProfileResource(Resource):
    @api.response(200, "Success", user_detail)
    @api.doc(description="Get user profile by ID")
    def get(self, user_id: int):
        """
        Метод для выдачи профили, у пользователя. .
        """
        session = Session()
        db_queries = QueriesDatabase(session)

        try:
            query = db_queries.get_user_profile(user_id=user_id)

            if query:
                return query, 200

        except Exception as e:
            return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

        finally:
            try:
                db_queries.close_session()
            except Exception as close_error:
                logger.error(f"Error closing session: {close_error}")


@api.route("/api/users/<int:following_id>/follow")
class FollowUserResource(Resource):
    def follow_process(self, following_id):
        session = Session()
        db_queries = QueriesDatabase(session)

        try:
            api_key: str = request.headers.get("api-key")

            if not api_key:
                logger.error(f"DELETE Запрос на /users/{following_id.id}/follow не обработан. Пользователь с ключом <{api_key}> не найден.")
                return {"result": False, "message": f"User with api_key{api_key} not found."}, 413

            query = db_queries.follow_processing_users(api_key=api_key, following_id=following_id)

            return query, 200

        except Exception as e:
            return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

        finally:
            try:
                db_queries.close_session()
            except Exception as close_error:
                logger.error(f"Error closing session: {close_error}")


    @api.response(200, "Success")
    @api.doc(description="Follow a user")
    def post(self, following_id):
        """
        Подписаться на пользователя.
        """

        return self.follow_process(following_id)

    @api.response(200, "Success")
    @api.doc(description="Unfollow a user")
    def delete(self, following_id):
        """
        Отписаться от пользователя.
        """

        return self.follow_process(following_id)
