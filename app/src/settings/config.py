import os

from dotenv import load_dotenv

UPLOAD_FOLDER = "/twitter-/static/images"
ALLOWED_EXTENSIONS = ["gif", "jpg", "jpeg", "png"]

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")