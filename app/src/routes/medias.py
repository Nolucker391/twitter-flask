from app.src.database.models import Session
from app.src.routes.FlaskAppSubSettings import api, logger
from app.src.schemas.schemas import media_response_model, media_upload_model
from app.src.utils.media_services import (
    QueriesDatabase,
    allowed_file,
)
from flask import request
from flask_restx import Resource


@api.route("/api/medias")
class MediaUploadResource(Resource):
    @api.expect(media_upload_model, validate=False)
    @api.response(200, "Success", media_response_model)
    @api.doc(description="Load media files")
    def post(self):
        """
        Функция-обработчик,  загрузки изображения к твиту.
        """
        session = Session()
        db_queries = QueriesDatabase(session)

        try:
            api_key = request.headers.get("api-key")
            media_file = request.files["file"]

            if not media_file or not allowed_file(media_file.filename):
                return {
                    "result": False,
                    "message": "Invalid file format or no file provided",
                }, 400
            image = db_queries.add_image_on_database(media_file=media_file, api_key=api_key)

            return {"result": True, "media_id": image}, 200

        except Exception as e:
            logger.error(f"Error in POST /api/medias: {e}")
            return {"result": False, "message": "Internal server error"}, 413

        finally:
            try:
                db_queries.close_session()
            except Exception as close_error:
                logger.error(f"Error closing session: {close_error}")
