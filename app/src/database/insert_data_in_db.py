# import datetime
import argparse

from sqlalchemy import insert
from models import User, ApiKey, Session, Tweets, Image, Like


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

tweets_data = [
    {"author_id": 1, "content": "My world! It's are first and test message on the messenger. Go to like on the post :D"},
    {"author_id": 2, "content": "Hey! I created a good messenger for communication ♥. Thanks my friend! Have a good day! ♡"},
    {"author_id": 3, "content": "I'm have a 200k on my balance Bitcoin!🤤🫡 Niiiceee!♡"},
    {"author_id": 4, "content": "I built a beast, a powerful gaming PC with the characteristics: RTX 4090, i9-14900K, 64GB Ram and M2 SSD for 2TB.💻"},
    {"author_id": 5, "content": "Come on 2025. The presidential position has been waiting for me. Good Luck."},
    {"author_id": 6, "content": "On CHILL, on Positive - I like the world... Bye!🤳"},
    {"author_id": 4, "content": "▁ ▂ ▄ ▅ ▆ ▇ █ 🄰🄳🅅🄴🅁🅃🄸🅂🄴🄼🄴🄽🅃 █ ▇ ▆ ▅ ▄ ▂ ▁"},
]

tweets_medias = [
    {"filename": 'babka.gif', "tweet_id": 1},
    {"filename": 'elon-musk-smoke.gif', "tweet_id": 2},
    {"filename": 'mellstroy.gif', "tweet_id": 3},
    {"filename": 'goodbro.gif', "tweet_id": 4},
    {"filename": 'trump-mewing-sigma.gif', "tweet_id": 5},
    {"filename": 'chill-guy-my-new-character.gif', "tweet_id": 6},
    {"filename": 'litvin.gif', "tweet_id": 6},
    {"filename": 'advertisement.gif', "tweet_id": 7},
]

likes_data = [
    {"user_id": 1, "tweet_id": 2},
    {"user_id": 1, "tweet_id": 3},
    {"user_id": 2, "tweet_id": 2},
    {"user_id": 2, "tweet_id": 1},
    {"user_id": 3, "tweet_id": 2},
    {"user_id": 3, "tweet_id": 4},
    {"user_id": 4, "tweet_id": 2},
    {"user_id": 4, "tweet_id": 6},
    {"user_id": 5, "tweet_id": 2},
    {"user_id": 5, "tweet_id": 5},
    {"user_id": 5, "tweet_id": 3},
    {"user_id": 6, "tweet_id": 2},
]

def insert_data():
    session = Session()
    session.execute(insert(User), users_data)
    session.execute(insert(ApiKey), users_api_data)
    session.execute(insert(Tweets), tweets_data)
    session.execute(insert(Image), tweets_medias)
    session.execute(insert(Like), likes_data)
    session.commit()  # Фиксируем изменения


if __name__ == "__main__":
    insert_data()