<img src="/TestImages/readme_media/11.png" alt="Demo" width="80" height="20"> <img src="/TestImages/readme_media/22.png" alt="Demo" width="80" height="20"> <img src="/TestImages/readme_media/33.png" alt="Demo" width="80" height="20"> <img src="/TestImages/readme_media/44.png" alt="Demo" width="80" height="20">

# <img src="/TestImages/readme_media/twitter.png" alt="Demo" width="50" height="50"> <sup>MicroService - Twitter</sup>

## Описание 

Этот проект представляет собой веб-сервис на базе нескольких инструментов, такие как Flask (Flask-RestX) приложение, сервера Nginx и базы данных PostgreSQL с движком SQLAlchemy. Все компоненты работают в контейнерах Docker и предназначены для взаимодействия с твитами, пользователями и медиафайлами. Сервис предоставляет пользователям возможность:

- **Загружать медиафайлы**.
- **Создавать и удалять твиты.**
- **Ставить и удалять лайки на твиты.**
- **Подписываться и отписываться от других пользователей.**
- **Получать информацию о пользователях и твитах.**

## Демо-версия

https://github.com/user-attachments/assets/d9dfcf79-e273-40b8-9707-0036dd4fde69

## Инструкция по запуску проекта 

1. Скопировать файлы проекта. Создать и войти в виртуальное окружение.
```commandline
git clone https://github.com/Nolucker391/twitter-flask.git
```

2. Установка необходимых зависимостей.
```commandline
pip install -r requirements.txt 

pip install --upgrade pip
```

3. Запуск проекта.
```commandline
docker compose up
```
<img src="/TestImages/readme_media/photo_5202193955649875263_y.jpg" alt="Demo" width="700" height="350"> <img src="/TestImages/readme_media/photo_5202193955649875267_y.jpg" alt="Demo" width="550" hei0ht="350">

4. Применение миграций и загрузка фикстур в БД.
```commandline
(Перед этим создаем директорию versions в папке alembic)

alembic revision --message="Init migration" --autogenerate

alembic upgrade head
```
<img src="/TestImages/readme_media/photo_5202193955649875269_y.jpg" alt="Demo" width="700" height="300">

Заполнение БД:
```commandline
docker exec -it twitter-flask-web-1 bash  - заходим в bash контейнера.

export PYTHONPATH=../src/:$PYTHONPATH  - создаем python-среду для импортов в директории.

python app/src/database/insert_data_in_db.py - указываем путь к insert_data_in_db
```
<img src="/TestImages/readme_media/photo_5202193955649875273_y.jpg" alt="Demo" width="700" height="300">

5. Автотестирование проекта.
```commandline

pytest /tests/
```
<img src="/TestImages/readme_media/photo_5202193955649875271_y.jpg" alt="Demo" width="700" height="300">


### Пользователи. 

Api-Key для входа        | Имя | Группа |
-----------------|-----------------|---------------|
test  |   test   |   Пользователь|
1111     |   ✔ Elon Musk [SpaceX]   |    Пользователь|
salfetka5      |   ⁂ Mellstroy Бурим ♛    |    Пользователь|
1234      |   ☏ HyperX Community ○   |        Пользователь       |
dk5      |   ✔【Trump】   |      Пользователь|
007      |   𓀥 Chill Guy ヅ   |      Пользователь|
