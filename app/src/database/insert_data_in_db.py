# import datetime
import argparse

from sqlalchemy import insert
from models import User, ApiKey, Session


users_data = [
    {"name": 'test'},
    {"name": '✔ Elon Musk [SpaceX]'},
    {"name": '⁂ Mellstroy | Бурим ♛'},
    {"name": '☏ HyperX Community ○'},
    {"name": '✔【Trump】'},
    {"name": '𓀥 Chill Guy ヅ'},
]

users_api_data = [
    {"user_id": 1, "api_key": 'test'},
    {"user_id": 2, "api_key": '1111'},
    {"user_id": 3, "api_key": 'salfetka5'},
    {"user_id": 4, "api_key": '1234'},
    {"user_id": 5, "api_key": 'dk5'},
    {"user_id": 6, "api_key": '007'},
]

def insert_data():
    session = Session()
    session.execute(insert(User), users_data)
    session.execute(insert(ApiKey), users_api_data)
    session.commit()  # Фиксируем изменения


if __name__ == "__main__":
    insert_data()