import os

from dotenv import load_dotenv

UPLOAD_FOLDER = "/twitter-/static/images"
ALLOWED_EXTENSIONS = ["gif", "jpg", "jpeg", "png"]

load_dotenv()

# Устанавливаем хост в зависимости от того, локально ли запускается приложение или в Docker
if os.environ.get("ENV") == "docker":
    DB_HOST = "postgres"
else:
    DB_HOST = "localhost"  # Локальный хост для работы вне контейнера

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
# DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
