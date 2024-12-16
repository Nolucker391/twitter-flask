from flask import request

from app.src.database.models import Session, User


def get_current_user_id():
    api_key = request.headers.get('api-key')
    session = Session()
    user = session.query(User).filter_by(api_key=api_key).first()
    session.close()
    return user.id if user else None

def get_user_by_id(user_id):
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    session.close()
    return user