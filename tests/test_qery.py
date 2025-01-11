# from app.src.database.models import Base, User
# from app.src.utils.user_services import QueriesDatabase
# from tests.test_add_data import app, test_engine
#
# def test_get_user_profile(db_session):
#     Base.metadata.create_all(test_engine)
#
#     # Создание тестового пользователя
#     user = User(id=1, name="test_user")
#     db_session.add(user)
#     db_session.commit()
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
