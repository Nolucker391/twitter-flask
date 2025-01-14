import logging

from app.src.schemas.schemas import (
    author_model,
    follower_model,
    following_model,
    like_model,
    media_response_model,
    media_upload_model,
    tweet_data_model,
    tweet_get_response_model,
    tweet_model,
    tweet_response_model,
    user_detail,
    user_information,
)
from flask import Flask
from flask_restx import Api

# Логирование ошибок
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder="/app/src/static")
api = Api(
    app,
    version="1.0",
    title="Twitter Service API",
    description="API for microblogging service",
)

api.models["TweetData"] = tweet_data_model
api.models["TweetResponse"] = tweet_response_model
# api.models['TweetGetResponse'] = tweet_get_response_model
api.models["MediaResponse"] = media_response_model
api.models["MediaUpload"] = media_upload_model

# разбиение по частям моделей у схемы для tweet_get_resp. Это нужно, если в схеме у нас несколько вложенных обектов (таблицы)
# в одной таблице (Например у твита есть связи через relation с другими табилцами, поэтому нужно эти таблицы тоже включить в схеме)
api.models["Author"] = author_model
api.models["Like"] = like_model
api.models["Tweet"] = tweet_model
api.models["TweetGetResponse"] = tweet_get_response_model

api.models["Follower"] = follower_model
api.models["Following"] = following_model
api.models["User"] = user_information
api.models["UserDetails"] = user_detail


# Взаимодействие с файлами
UPLOAD_FOLDER = "../src/app/static/medias/user_api"
# UPLOAD_FOLDER = os.path.join(app.root_path, '..', 'app', 'medias')
ALLOWED_EXTENSIONS = {"gif", "jpg", "jpeg", "png"}
