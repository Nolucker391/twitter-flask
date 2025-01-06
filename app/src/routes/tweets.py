from flask import request
from flask_restx import Resource
from sqlalchemy import insert, select, Sequence, update

from app.src.database.models import User, ApiKey, Session, Tweets, Image
# from app.src.utils.tweet_services import get_author_id
from app.src.schemas.schemas import tweet_data_model, tweet_response_model

from app.src.routes.FlaskAppSubSettings import api

@api.route("/api/tweets")
class TweetResource(Resource):
    @api.expect(tweet_data_model, validate=True)
    @api.response(200, "Success", tweet_response_model)
    @api.doc(description="Create a new tweet")
    def post(self):
        """
        Create a new tweet
        """
        api_key = request.headers.get("api-key")
        session = Session()
        query = session.query(User).join(ApiKey).filter(ApiKey.api_key == api_key).first()
        tweet_data = request.json
        query2 = session.execute(insert(Tweets).values(author_id=query.id, content=tweet_data.get("tweet_data")).returning(Tweets.id))
        session.commit()
        tweet_id = query2.scalar_one_or_none()
        media_ids = tweet_data.get("tweet_media_ids")
        if media_ids:
            for m_id in media_ids:
                session.execute(update(Image).where(Image.id == m_id).values(tweet_id=tweet_id))
                session.commit()
        response_data = {
            "result": True,
            "tweet_id": tweet_id,
        }
        return response_data, 200

    from typing import Sequence
    def get(self):
        session = Session()
        query_tweets = session.execute(select(Tweets)).scalars().all()
        # test_Unknown.jpeg

        response_data = {
            "result": True,
            "tweets": [
                {
                    "id": tweet.id,
                    "content": tweet.content,
                    "attachments": [
                        f"static/medias/{link.filename}" for link in tweet.attachments
                    ],
                    "author": {
                        "id": tweet.author_id,
                        "name": "string"
                    },
                    "likes": [
                        {
                            "user_id": 0,
                            "name": "string"
                        }
                    ]
                } for tweet in query_tweets
            ]
        }

        return response_data, 200

#
# @api.route("/api/tweets/<int:id>")
# class TweetIdResource(Resource):
#     @api.response(200, "Success")
#     @api.doc(description="Delete a tweet")
#     def delete(self, id):
#         """
#         Delete a tweet
#         """
#         # author_id = get_current_user_id()
#         # tweet_service.delete_tweet(id, author_id)
#         return {"result": True}, 200
