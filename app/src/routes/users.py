from flask import request, jsonify
from flask_restx import Resource

from app.src.routes.FlaskAppSubSettings import api, logger
from sqlalchemy import delete, insert, select, update
from app.src.database.models import ApiKey, Session, User, user_following
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



@api.route("/api/users/<int:following_id>/follow")
class FollowUserResource(Resource):
    def follow_process(self, following_id, query_method):
        session = Session()
        # db_queries = QueriesDatabase(session)
        try:
            api_key: str = request.headers.get("api-key")
            user = session.query(User).join(ApiKey).filter(ApiKey.api_key == api_key).first()

            if not api_key:
                logger.error(f"DELETE Запрос на /users/{user.id}/follow не обработан. Пользователь с ключом <{api_key}> не найден.")
                return {"result": False, "message": f"User with api_key{api_key} not found."}, 413

            select_user_query = select(User).where(User.id == following_id)
            user_to_follow = session.execute(select_user_query)
            user_to_follow = user_to_follow.scalar_one_or_none()

            if user_to_follow:
                exist_follow = session.execute(
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
                    session.execute(stmt)
                    session.commit()

                    return {"result": True}
                    # return {
                    #     "result": False,
                    #     "error_message": f"Пользователь с id={user.id} уже подписан на пользователя с id={following_id}",
                    #     "error_type": "FollowExist",
                    # }

                else:
                    stmt = insert(user_following).values(user_id=user.id, following_id=following_id)
                    session.execute(stmt)
                    session.commit()

                    return {"result": True}

        except Exception as e:
            pass

    @api.response(200, "Success")
    @api.doc(description="Follow a user")
    def post(self, following_id):
        """
        Follow a user
        """

        return self.follow_process(following_id, query_method="follow")

    @api.response(200, "Success")
    @api.doc(description="Unfollow a user")
    def delete(self, following_id):
        """
        Unfollow a user
        """

        return self.follow_process(following_id, query_method="unfollow")
