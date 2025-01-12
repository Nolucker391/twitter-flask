import json

import pytest
from app.src.routes.FlaskAppSubSettings import app
from tests.conftest import TEST_DATABASE_URI

myapp = app

@pytest.fixture
def app():
    _app = myapp
    _app.config["TESTING"] = True

    yield _app


@pytest.fixture
def client(app):
    """Фикстура для создания тестового клиента Flask."""
    client = app.test_client()
    yield client


def test_status_code_for_users_me(client):
    """Тестирование статус-кода эндпоинта /api/users/me."""
    response = client.get(
        "/api/tweets",  # Укажите нужные заголовки
    )
    print(response.data)
    # Проверяем статус-код
    # assert response.status_code == 200