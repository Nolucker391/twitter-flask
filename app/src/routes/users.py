from flask import request, jsonify
from flask_restx import Resource

from app.src.routes.FlaskAppSubSettings import api
from sqlalchemy import delete, insert, select, update
from app.src.database.models import ApiKey, Session, User
from sqlalchemy.exc import SQLAlchemyError


@api.route("/api/users/me")
class CurrentUserResource(Resource):
    @api.response(200, "Success")
    @api.doc(description="Get current user's profile")
    def get(self):
        """
        Метод для выдачи информации о пользователе на главной странице.
        """
        try:
            api_key = request.headers.get("Api-Key")
            session = Session()
            # query = session.query(ApiKey).filter_by(api_key=api_key).first()
            # query2 = session.query(User).filter_by(id=query.user_id).first()
            query = session.query(User).join(ApiKey).filter(ApiKey.api_key == api_key).first()

            if not query:
                return jsonify({"error": "Пользователь с таким API не найден."}), 401
            a = {
                "result": True,
                "user": {
                    "id": query.id,
                    "name": query.name,
                    "followers": [],
                    "following": []
                }
            }

            a["user"]["followers"] = [
                {
                    "id": f.id,
                    "name": f.name
                }
                for f in query.followers
            ]

            a["user"]["following"] = [
                {
                    "id": f.id,
                    "name": f.name
                }
                for f in query.following
            ]

            return a, 200

        except Exception as e:
            return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@api.route("/api/users/<int:user_id>")
class UserProfileResource(Resource):
    @api.response(200, "Success")
    @api.doc(description="Get user profile by ID")
    def get(self, user_id: int):
        """
        Метод для выдачи профили, у пользователя. .
        """

        try:
            session = Session()
            query = session.query(User).filter_by(id=user_id).first()

            if not query:
                return jsonify({"error": "Пользователь с таким ID не найден."}), 401
            a = {
                "result": True,
                "user": {
                    "id": query.id,
                    "name": query.name,
                    "followers": [],
                    "following": []
                }
            }

            a["user"]["followers"] = [
                {
                    "id": f.id,
                    "name": f.name
                }
                for f in query.followers
            ]

            a["user"]["following"] = [
                {
                    "id": f.id,
                    "name": f.name
                }
                for f in query.following
            ]

            return a, 200

        except Exception as e:
            return jsonify({"error": f"Unexpected error: {str(e)}"}), 500



@api.route("/api/users/<int:user_id>/follow")
class FollowUserResource(Resource):
    def follow_process(self, user_id, query_method):
        session = Session()
        # db_queries = QueriesDatabase(session)
        pass

    @api.response(200, "Success")
    @api.doc(description="Follow a user")
    def post(self, user_id):
        """
        Follow a user
        """

        return self.follow_process(user_id, query_method="follow")

    @api.response(200, "Success")
    @api.doc(description="Unfollow a user")
    def delete(self, user_id):
        """
        Unfollow a user
        """

        return self.follow_process(user_id, query_method="unfollow")
