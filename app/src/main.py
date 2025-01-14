from app.src.database.models import Base, engine
from app.src.routes.FlaskAppSubSettings import app, logger

if __name__ == "__main__":
    Base.metadata.create_all(engine)

    logger.info("Запуск приложения Clone Twitter...")

    app.run(debug=True, host="0.0.0.0", port=8000)
