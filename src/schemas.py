from flask_restx import Namespace, fields

# создание пространства имен API для операций с твитами
api = Namespace("tweets", description="Tweet related operations")

# определение моделей данных для входящих данных твитов, которую ожидает API
tweet_data_model = api.model("TweetData", {
    "tweet_data": fields.String(description="Content of the tweet", required=True),
    "tweet_media_ids": fields.List(fields.Integer, description="Optional list of media IDs attached to the tweet")
})

tweet_response_model = api.model("TweetResponse", {
    "result": fields.Boolean(description="Status of the operation"),
    "tweet_id": fields.Integer(description="ID of the created tweet")
})