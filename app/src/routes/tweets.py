from flask import request
from flask_restx import Resource

from app.src.utils.tweet_services import get_author_id
from app.src.schemas.schemas import tweet_data_model, tweet_response_model

from app.src.routes.FlaskAppSubSettings import api, tweet_service

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
        print("aaaa", tweet_id)
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


@api.route("/api/tweets/<int:id>")
class TweetIdResource(Resource):
    @api.response(200, "Success")
    @api.doc(description="Delete a tweet")
    def delete(self, id):
        """
        Delete a tweet
        """
        # author_id = get_current_user_id()
        # tweet_service.delete_tweet(id, author_id)
        return {"result": True}, 200
