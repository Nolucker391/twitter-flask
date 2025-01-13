from app.src.database.models import metadata


def test_database_connection(db_session):
    """Простой тест для проверки подключения к базе данных."""
    metadata.reflect(bind=db_session.bind)  # Указываем bind явно
    tables = metadata.tables.keys()

    print("Таблицы в базе данных (ORM):", list(tables))

    assert len(tables) > 0  # Убедитесь, что таблицы существуют
