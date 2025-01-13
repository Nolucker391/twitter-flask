import pytest
import subprocess

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from alembic.config import Config
from alembic import command


# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# export PYTHONPATH=../twitter-flask/:$PYTHONPATH

DB_HOST_TEST = "localhost"
DB_PORT_TEST = 5433
DB_NAME_TEST = "test_db"
DB_USER_TEST = "test_user"
DB_PASS_TEST = "test_password"

data = {
    "names": ["John", "Smith", "Stive"],
    "api-keys": ["dk5", 123, 5666],
    "filename": ["test_path.png", "test_path.jpg"],
    "content": ["Hello world!", "test message."]
}

TEST_DATABASE_URI = f"postgresql+psycopg2://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"
test_engine = create_engine(TEST_DATABASE_URI, echo=False)
TestSession = scoped_session(sessionmaker(bind=test_engine))

def create_migration_if_needed():
    """
    Функция для создания миграции.
    Используем subprocess для вызова Alembic через командную строку.
    """
    try:
        print("Пытаемся создать миграцию...")
        subprocess.run(
            [
                "alembic",
                "-c", "../twitter-flask/alembic_for_test/alembic.ini",
                "revision", "--autogenerate", "-m", "auto migration"
            ],
            check=True
        )
        print("Миграция успешно создана!")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании миграции: {e}")

def apply_migrations(database_uri):
    """
    Применение миграций с использованием Alembic.
    """
    alembic_cfg = Config("../twitter-flask/alembic_for_test/")
    alembic_cfg.set_main_option("sqlalchemy.url", database_uri)

    alembic_cfg.set_main_option("script_location", "../twitter-flask/alembic_for_test/alembic/")  # Убедитесь, что этот путь правильный

    create_migration_if_needed()    # Сначала создаём миграцию, если нужно

    command.upgrade(alembic_cfg, "head")  # Применяем миграции до последней версии

@pytest.fixture(scope="session")
def test_db():
    """
    Фикстура для создания тестовой базы данных перед тестами.
    """

    # Применяем миграции для тестовой базы данных
    apply_migrations(TEST_DATABASE_URI)
    yield
    print("Миграции применены и база готова для тестов")
    # # После тестов очищаем базу
    # Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(scope="function")
def db_session(test_db):
    """Фикстура для предоставления сессии базы данных."""
    session = TestSession()

    try:
        yield session
    finally:
        session.rollback()
        session.close()

# from app.src.database.models import metadata
# def test_database_connection(db_session):
#     """Простой тест для проверки подключения к базе данных."""
#     metadata.reflect(bind=db_session.bind)  # Указываем bind явно
#     tables = metadata.tables.keys()
#
#     print("Таблицы в базе данных (ORM):", list(tables))
#
#     assert len(tables) > 0  # Убедитесь, что таблицы существуют
