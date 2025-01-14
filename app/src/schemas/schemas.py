from flask_restx import Namespace, fields

# создание пространства имен API для операций с твитами
api = Namespace("tweets", description="Tweet related operations")

# определение моделей данных для входящих данных твитов, которую ожидает API

# Модель запроса для POST /api/tweets/
tweet_data_model = api.model(
    "TweetData",
    {
        "tweet_data": fields.String(description="Content of the tweet", required=True),
        "tweet_media_ids": fields.List(
            fields.Integer,
            description="Optional list of media IDs attached to the tweet",
        ),
    },
)

tweet_response_model = api.model(
    "TweetResponse",
    {
        "result": fields.Boolean(description="Status of the operation"),
        "tweet_id": fields.Integer(description="ID of the created tweet"),
    },
)

# Модель запроса для POST /api/medias/
media_upload_model = api.model(
    "MediaUpload",
    {
        "file": fields.Raw(required=True, description="Media file to upload"),
    },
)

# Модель ответа для GET /api/medias/ и POST /api/medias/
media_response_model = api.model(
    "MediaResponse",
    {
        "result": fields.Boolean(required=True, description="Result status"),
        "media_id": fields.Integer(required=True, description="ID of the media"),
    },
)

author_model = api.model(
    "Author",
    {
        "id": fields.Integer(required=True, description="ID of the author"),
        "name": fields.String(required=True, description="Name of the author"),
    },
)

# 2. Модель для "Like"
like_model = api.model(
    "Like",
    {
        "user_id": fields.Integer(
            required=True, description="ID of the user who liked the tweet"
        ),
        "name": fields.String(
            required=True, description="Name of the user who liked the tweet"
        ),
    },
)

# 3. Модель для "Tweet"
tweet_model = api.model(
    "Tweet",
    {
        "id": fields.Integer(required=True, description="ID of the tweet"),
        "content": fields.String(required=True, description="Content of the tweet"),
        "attachments": fields.List(
            fields.String, required=True, description="List of media file URLs"
        ),
        "author": fields.Nested(
            author_model, required=True, description="Author information"
        ),
        "likes": fields.List(
            fields.Nested(like_model), required=False, description="List of likes"
        ),
    },
)

# 4. Модель для "TweetGetResponse" запроса для GET /api/tweets/
tweet_get_response_model = api.model(
    "TweetGetResponse",
    {
        "result": fields.Boolean(required=True, description="Result status"),
        "tweets": fields.List(
            fields.Nested(tweet_model),
            required=True,
            description="List of tweets with attachments",
        ),
    },
)

# Модель "Follower" для "UserDetails"
follower_model = api.model(
    "Follower",
    {
        "id": fields.Integer(required=True, description="ID of the follower"),
        "name": fields.String(required=True, description="Name of the follower"),
    },
)

# Модель "Following" для "UserDetails"
following_model = api.model(
    "Following",
    {
        "id": fields.Integer(
            required=True, description="ID of the user being followed"
        ),
        "name": fields.String(
            required=True, description="Name of the user being followed"
        ),
    },
)

# Модель "UserDetails" для "User"
user_detail = api.model(
    "UserDetails",
    {
        "id": fields.Integer(required=True, description="ID of the user"),
        "name": fields.String(required=True, description="Name of the user"),
        "followers": fields.List(
            fields.Nested(follower_model),
            required=True,
            description="List of followers",
        ),
        "following": fields.List(
            fields.Nested(following_model),
            required=True,
            description="List of users being followed",
        ),
        # "tweets": fields.List(fields.Nested(tweet_model), required=True, description="List of tweets posted by the user")
    },
)

# Модель запроса для GET /api/users/me и /api/users/<int:user_id>
user_information = api.model(
    "User",
    {
        "result": fields.Boolean(required=True, description="Result status"),
        "user": fields.Nested(
            user_detail, required=True, description="Detailed user information"
        ),
    },
)

# # Модель запроса для GET /api/tweets/
# tweet_get_response_model = api.model("TweetGetResponse", {
#     "result": fields.Boolean(required=True, description="Result status"),
#     "tweets": fields.List(fields.Nested(api.model("Tweet", {
#         "id": fields.Integer(required=True, description="ID of the tweet"),
#         "content": fields.String(required=True, description="Content of the tweet"),
#         "attachments": fields.List(fields.String, required=True, description="List of media file URLs"),
#         "author": fields.Nested(api.model("Author", {
#             "id": fields.Integer(required=True, description="ID of the author"),
#             "name": fields.String(required=True, description="Name of the author"),
#         }), required=True, description="Author information"),
#         "likes": fields.List(fields.Nested(api.model("Like", {
#             "user_id": fields.Integer(required=True, description="ID of the user who liked the tweet"),
#             "name": fields.String(required=True, description="Name of the user who liked the tweet"),
#         })), required=False, description="List of likes")
#     })), required=True, description="List of tweets with attachments"),
# })
