import os
import time

from app.src.database.models import Image
from app.src.routes.FlaskAppSubSettings import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, logger
from sqlalchemy import insert, select


def allowed_file(filename):
    """Функция, для проверки, загружаемого файла, допустимого формата."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_image_on_system(media_file, api_key) -> str:
    """Функция, для сохранения изображения в системе проекта."""
    try:
        out_file_path = f"{UPLOAD_FOLDER}_{api_key}"  # путь в контейнере
        file_path = os.path.join(out_file_path, media_file.filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        if os.path.exists(file_path):
            base, ext = os.path.splitext(media_file.filename)
            unique_filename = f"{base}_{int(time.time())}{ext}"
            file_path = os.path.join(out_file_path, unique_filename)

            media_file.save(file_path)

            return unique_filename

        media_file.save(file_path)

        return media_file.filename

    except Exception as e:
        logger.error(f"Error saving image to system: {e}")
        raise


class QueriesDatabase:
    def __init__(self, session):
        """Инициализация сессии базы данных."""
        self.session = session

    def get_image(self, filename):
        """Функция, для просмотра изображения на опубликованный твит."""
        try:
            query = select(Image).where(Image.filename == filename)
            result = self.session.execute(query).scalar_one_or_none()

            return result

        except Exception as e:
            logger.error(f"Error fetching image from database: {e}")

            return None

    def add_image_on_database(self, media_file, api_key):
        """
        Функция, для добавления в БД - изображения к твиту.
        Загружаемый файл не должно превышать: 1МБ
        """
        try:
            file_path = save_image_on_system(media_file=media_file, api_key=api_key)

            if file_path:
                query = insert(Image).values(filename=file_path).returning(Image.id)
                result = self.session.execute(query)
                self.session.commit()
                image_id = result.scalar_one()

                return image_id

        except Exception as e:
            logger.error(f"Error adding image to database: {e}")
            self.session.rollback()

            return None

    def close_session(self):
        """Закрыть сессию после завершения работы."""
        self.session.close()
