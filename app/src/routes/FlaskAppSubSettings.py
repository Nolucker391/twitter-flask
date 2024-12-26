import logging

from flask import Flask
from flask_restx import Api

from app.src.schemas.schemas import tweet_data_model, tweet_response_model

logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='/app/src/static')
api = Api(app, version="1.0", title="Twitter Service API", description="API for microblogging service")

api.models['TweetData'] = tweet_data_model
api.models['TweetResponse'] = tweet_response_model

