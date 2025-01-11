import pytest
import os
import sys
from flask import Flask

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.src.database.models import Base

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


DB_HOST_TEST = "localhost"
DB_PORT_TEST = 5433
DB_NAME_TEST = "test_db"
DB_USER_TEST = "test_user"
DB_PASS_TEST = "test_password"

TEST_DATABASE_URI = f"postgresql+psycopg2://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"
test_engine = create_engine(TEST_DATABASE_URI, echo=False)
TestSession = scoped_session(sessionmaker(bind=test_engine))


@pytest.fixture(scope="session")
def app():
    """Создание Flask-приложения для тестов."""
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = TEST_DATABASE_URI
    return app

@pytest.fixture(scope="session")
def test_db():
    """Создание схемы тестовой базы данных перед тестами."""
    Base.metadata.create_all(test_engine)
    yield
    Base.metadata.drop_all(test_engine)

@pytest.fixture(scope="function")
def db_session(test_db):
    """Фикстура для предоставления сессии базы данных."""
    session = TestSession()

    try:
        yield session
    finally:
        session.rollback()
        session.close()

from app.src.database.models import Base, User
from app.src.utils.user_services import QueriesDatabase

def test_get_user_profile(db_session):
    Base.metadata.create_all(test_engine)

    # Создание тестового пользователя
    user = User(id=1, name="test_user")
    db_session.add(user)
    db_session.commit()
#
#     with app.test_client() as client:
#         db_queries = QueriesDatabase(db_session)
#
#         result = db_queries.get_user_profile(user_id=1)
#         assert result["result"] is True
#         assert result["user"]["name"] == "test_user"
#
#         # Запрос несуществующего пользователя
#         result = db_queries.get_user_profile(user_id=999)
#         assert result[1] == 401
