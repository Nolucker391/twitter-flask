import logging
from flask import Flask, request
from flask_restx import Api, Resource

from src.models import Base, engine
from src.schemas import tweet_data_model, tweet_response_model
from src.tweet_services import get_author_id, TweetService


logger = logging.getLogger(__name__)
app = Flask(__name__, static_folder='/src/static')
api = Api(app, version="1.0", title="Twitter Service API", description="API for microblogging service")
api.models['TweetData'] = tweet_data_model
api.models['TweetResponse'] = tweet_response_model

tweet_service = TweetService(Base)



from src.models import Session, User

def get_current_user_id():
    api_key = request.headers.get('api-key')
    session = Session()
    user = session.query(User).filter_by(api_key=api_key).first()
    session.close()
    return user.id if user else None

def get_user_by_id(user_id):
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    session.close()
    return user

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
            "id": 0,
            "name": "string",
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
        return b, 200

@api.route("/api/tweets")
class TweetResource(Resource):
    @api.expect(tweet_data_model, validate=True)
    @api.response(200, "Success", tweet_response_model)
    @api.doc(description="Create a new tweet")
    def post(self):
        """
        Create a new tweet
        """
        tweet_data = request.json
        author_id = get_author_id()
        tweet_id = tweet_service.create_tweet(tweet_data, author_id)
        print(tweet_id)
        response_data = {
            "result": True,
            "tweet_id": tweet_id,
        }
        return response_data, 200

    def get(self):
        response_data = {
            "result": True,
            "tweets": [
                {
                    "id": 0,
                    "content": "string",
                    "attachments": [
                        "string"
                    ],
                    "author": {
                        "id": 0,
                        "name": "string"
                    },
                    "likes": [
                        {
                            "user_id": 0,
                            "name": "string"
                        }
                    ]
                }
            ]
        }
        return response_data, 200

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    logger.info("Запуск приложения Clone Twitter...")
    app.run(debug=True, host="0.0.0.0", port=8000)


