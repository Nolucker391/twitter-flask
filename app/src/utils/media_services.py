import os

from sqlalchemy import select, insert

from app.src.routes.FlaskAppSubSettings import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, logger
from app.src.database.models import Image


def allowed_file(filename):
    """ Функция, для проверки, загружаемого файла, допустимого формата. """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image_on_system(media_file, api_key) -> None:
    """ Функция, для сохранения изображения в системе проекта. """
    try:
        out_file_path = f"{UPLOAD_FOLDER}_{api_key}"  # путь в контейнере
        file_path = os.path.join(out_file_path, media_file.filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        if not os.path.exists(out_file_path):
           logger.info(f"Directory {out_file_path} does not exist!")

        media_file.save(file_path)

    except Exception as e:
        logger.error(f"Error saving image to system: {e}")
        raise


class QueriesDatabase:
    def __init__(self, session):
        """Инициализация сессии базы данных."""
        self.session = session

    def get_image(self, filename):
        """ Функция, для просмотра изображения на опубликованный твит. """
        try:
            query = select(Image).where(Image.filename == filename)
            result = self.session.execute(query).scalar_one_or_none()

            return result

        except Exception as e:
            logger.error(f"Error fetching image from database: {e}")

            return None

    def add_image_on_database(self, filename):
        """ Функция, для добавления в БД - изображения к твиту. """
        try:
            query = insert(Image).values(filename=filename).returning(Image.id)
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


