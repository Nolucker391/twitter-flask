import logging
from flask import Flask, request
from flask_restx import Api, Resource

from src.models import Base, engine
from src.schemas import tweet_data_model, tweet_response_model
from src.tweet_services import get_author_id, TweetService


logger = logging.getLogger(__name__)
app = Flask(__name__, static_url_path="/static")
api = Api(app, version="1.0", title="Twitter Service API", description="API for microblogging service")
api.models['TweetData'] = tweet_data_model
api.models['TweetResponse'] = tweet_response_model

tweet_service = TweetService(Base)


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


