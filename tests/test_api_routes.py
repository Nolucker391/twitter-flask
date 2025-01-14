import json

import pytest
from app.src.routes.FlaskAppSubSettings import app

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


def test_get_user_me(client):
    """Тестовый запрос на endpoint /api/users/me"""
    headers = {"api-key": "test"}
    response = client.get(
        "/api/users/me",
        headers=headers,
    )

    assert response.status_code == 200
    response_data = json.loads(response.text)

    assert response_data["result"] is True
    assert "user" in response_data
    user_data = response_data["user"]

    assert user_data["id"] == 1
    assert user_data["name"] == "test"

    # Проверяем, что followers и following — списки
    assert isinstance(user_data["followers"], list)
    assert isinstance(user_data["following"], list)


def test_get_user_profile(client):
    """Тестовый запрос на endpoint /api/users/<int:user_id>"""
    headers = {"api-key": "test"}
    response = client.get("/api/users/1", headers=headers)

    assert response.status_code == 200
    response_data = json.loads(response.text)

    # Проверяем структуру ответа
    assert response_data["result"] is True
    assert "user" in response_data
    user_data = response_data["user"]

    assert user_data["id"] == 1
    assert user_data["name"] == "test"

    # Проверяем, что followers и following — списки
    assert isinstance(user_data["followers"], list)
    assert isinstance(user_data["following"], list)


def test_following_process_user(client):
    """Тестовый запрос на endpoint /api/users/<int:user_id>/follow"""
    # Подписываемся на пользователя.
    headers = {"api-key": "test"}
    response = client.post("/api/users/6/follow", headers=headers)
    assert response.status_code == 200
    assert json.loads(response.text) == {"result": True}

    # Проверяем подписку.
    response_get = client.get("/api/users/me", headers=headers)

    assert response.status_code == 200
    response_data_get = json.loads(response_get.text)
    assert response_data_get["result"] is True
    following = response_data_get["user"]["following"]

    assert any(
        follow.get("id") == 6 and follow.get("name") == "𓀥 Chill Guy ヅ"
        for follow in following
    ), "Пользователь с id=6 и name='𓀥 Chill Guy ヅ' отсутствует в following"

    # Отписываемся от пользователя.
    response_del = client.delete("/api/users/6/follow", headers=headers)
    assert response_del.status_code == 200
    assert json.loads(response_del.text) == {"result": True}


def test_get_post_tweets(client):
    """Тестовый запрос на добавление, удаление и отображения твита."""
    # Создаем новый твит.
    headers = {"api-key": "test"}
    response = client.post(
        "/api/tweets",
        headers=headers,
        json={"tweet_data": "Тестовый текст.", "tweet_media_ids": [1, 2]},
    )
    assert response.status_code == 200
    assert "tweet_id" in response.json

    response_data = response.json
    tweet_id = response_data["tweet_id"]
    assert tweet_id is not None

    # Смотрим добавился ли наш твит.
    response_get_tweet = client.get(
        "/api/tweets",
        headers=headers,
    )

    assert response_get_tweet.status_code == 200
    response_data_get = json.loads(response_get_tweet.text)

    assert any(
        i.get("content") == "Тестовый текст." for i in response_data_get["tweets"]
    )

    # Удаляем наш созданный твит.
    response_delete = client.delete(
        f"/api/tweets/{tweet_id}",
        headers=headers,
    )
    assert response_delete.status_code == 200
    assert json.loads(response_delete.text) == {"result": True}


def test_post_del_likes(client):
    """Тестовый запрос на добавление и удаления лайка твита."""
    # Ставим лайк
    headers = {"api-key": "test"}
    response_post = client.post(
        "/api/tweets/1/likes",
        headers=headers,
    )
    assert response_post.status_code == 200
    assert json.loads(response_post.text) == {"result": True}

    # Удаляем лайк
    response_del = client.delete(
        "/api/tweets/1/likes",
        headers=headers,
    )
    assert response_del.status_code == 200
    assert json.loads(response_del.text) == {"result": True}


def test_post_media(client):
    """Тестовый запрос на загрузку фото к твиту."""
    with open("tests/image/test.png", "rb") as file:
        data = {"file": (file, "test.png")}
        response = client.post(
            "/api/medias", data=data, content_type="multipart/form-data"
        )
        response_data = json.loads(response.text)
        assert response.status_code == 200
        assert response_data["result"] is True
        assert isinstance(response_data["result"], int) is True
