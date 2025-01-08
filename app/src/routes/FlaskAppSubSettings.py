import logging

from flask import Flask
from flask_restx import Api

from app.src.schemas.schemas import (
    tweet_data_model,
    tweet_response_model,
    tweet_get_response_model,
    media_response_model,
    media_upload_model,
)

# Логирование ошибок
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='/app/src/static')
api = Api(app, version="1.0", title="Twitter Service API", description="API for microblogging service")

api.models['TweetData'] = tweet_data_model
api.models['TweetResponse'] = tweet_response_model
api.models['TweetGetResponse'] = tweet_get_response_model
api.models['MediaResponse'] = media_response_model
api.models['MediaData'] = media_upload_model

# Взаимодействие с файлами
UPLOAD_FOLDER = "../src/app/static/medias/user_api"
# UPLOAD_FOLDER = os.path.join(app.root_path, '..', 'app', 'medias')
ALLOWED_EXTENSIONS = {"gif", "jpg", "jpeg", "png"}
