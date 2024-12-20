from flask import request
from flask_restx import Resource

from app.src.routes.FlaskAppSubSettings import api
from sqlalchemy import delete, insert, select, update
from app.src.database.models import ApiKey, Session


@api.route("/api/users/me")
class CurrentUserResource(Resource):
    @api.response(200, "Success")
    @api.doc(description="Get current user's profile")
    def get(self):
        """
        Get current user's profile
        """
        # user_id = get_current_user_id()
        # user_profile = tweet_service.get_current_user_profile(user_id)
        api_key = request.headers.get("api-key")
        query = select(ApiKey).where(ApiKey.api_key == api_key)
        key = Session.execute(query)
        key = key.scalars().one_or_none()

        if key:
            print(key.user_id)
        else:
            print("Не нашлось")

        a = {
            "result": True,
            "user": {
                "id": 1,
                "name": "test",
                "followers": [
                    {
                        "id": 0,
                        "name": "string"
                    }
                ],
                "following": [
                    {
                        "id": 0,
                        "name": "string"
                    }
                ]
            }
        }
        # return {"result": True, "user": user_profile}, 200
        return a, 200


@api.route("/api/users/<int:id>")
class UserProfileResource(Resource):
    @api.response(200, "Success")
    @api.doc(description="Get user profile by ID")
    def get(self, user_id):
        """
        Get user profile by ID
        """
        # user = get_user_by_id(user_id)
        # if user:
        #     return {"result": True, "user": {
        #         "id": user.id,
        #         "name": user.name}}, 200
        # else:
        #     return {"result": False, "message": "User not found"}, 404

        b = {
            "result": True,
            "user": {
                "id": 1,
                "name": "string",
                "followers": [
                    {
                        "id": 2,
                        "name": "string"
                    }
                ],
                "following": [
                    {
                        "id": 0,
                        "name": "string"
                    }
                ]
            }
        }

        return b, 200

@api.route("/api/users/<int:id>/follow")
class FollowUserResource(Resource):
    @api.response(200, "Success")
    @api.doc(description="Follow a user")
    def post(self, id):
        """
        Follow a user
        """
        # follower_id = get_current_user_id()
        # tweet_service.follow_user(id, follower_id)
        return {"result": True}, 200

    @api.response(200, "Success")
    @api.doc(description="Unfollow a user")
    def delete(self, id):
        """
        Unfollow a user
        """
        # follower_id = get_current_user_id()
        # tweet_service.unfollow_user(id, follower_id)
        return {"result": True}, 200
