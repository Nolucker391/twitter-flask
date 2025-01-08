from flask_restx import Namespace, fields

# создание пространства имен API для операций с твитами
api = Namespace("tweets", description="Tweet related operations")

# определение моделей данных для входящих данных твитов, которую ожидает API

# Модель запроса для POST /api/tweets/
tweet_data_model = api.model("TweetData", {
    "tweet_data": fields.String(description="Content of the tweet", required=True),
    "tweet_media_ids": fields.List(fields.Integer, description="Optional list of media IDs attached to the tweet")
})

tweet_response_model = api.model("TweetResponse", {
    "result": fields.Boolean(description="Status of the operation"),
    "tweet_id": fields.Integer(description="ID of the created tweet")
})

# Модель запроса для GET /api/tweets/
tweet_get_response_model = api.model("MediaGETResponse", {
    "result": fields.Boolean(required=True, description="Result status"),
    "tweets": fields.List(fields.Nested(api.model("Tweet", {
        "id": fields.Integer(required=True, description="ID of the tweet"),
        "content": fields.String(required=True, description="Content of the tweet"),
        "attachments": fields.List(fields.String, required=True, description="List of media file URLs"),
        "author": fields.Nested(api.model("Author", {
            "id": fields.Integer(required=True, description="ID of the author"),
            "name": fields.String(required=True, description="Name of the author"),
        }), required=True, description="Author information"),
        "likes": fields.List(fields.Nested(api.model("Like", {
            "user_id": fields.Integer(required=True, description="ID of the user who liked the tweet"),
            "name": fields.String(required=True, description="Name of the user who liked the tweet"),
        })), required=False, description="List of likes")
    })), required=True, description="List of tweets with attachments"),
})

# Модель запроса для POST /api/medias/
media_upload_model = api.model("MediaUpload", {
    "file": fields.Raw(required=True, description="Media file to upload"),
})

# Модель ответа для GET /api/medias/ и POST /api/medias/
media_response_model = api.model("MediaResponse", {
    "result": fields.Boolean(required=True, description="Result status"),
    "media_id": fields.Integer(required=True, description="ID of the media"),
})







