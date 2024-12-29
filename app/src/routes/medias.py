import os

from flask import request
from flask_restx import Resource
from sqlalchemy import select, insert


from app.src.routes.FlaskAppSubSettings import api, app
from app.src.database.models import ApiKey, Session, User, Image

UPLOAD_FOLDER = "../twitter-flask/app/medias"
ALLOWED_EXTENSIONS = ["gif", "jpg", "jpeg", "png"]


def get_image(filename, session):
    query = session.execute(select(Image)).where(Image.filename == filename)
    image = query.scalars().one_or_none()
    return image


def add_image_on_database(filename, session):
    query = session.execute(insert(Image)).values(filename=filename).returning(Image.id)
    session.commit()
    image_id = query.scalar_one()
    return image_id


def save_image(out_file_path, file):
    file_path = os.path.join(out_file_path, file.filename)
    file.save(file_path)


@api.route("/api/medias")
class MediaUploadResource(Resource):
    @api.doc(description="Load media files")
    def post(self):
        """
        Load media files
        """
        api_key = request.headers.get("api-key")
        session = Session()
        query = session.query(User).join(ApiKey).filter(ApiKey.api_key == api_key).first()
        media_file = request.files["file"]
        filename = f"{api_key}_{media_file.filename}"

        image = get_image(filename=filename, session=session)

        if not image:
            image_id = add_image_on_database(filename=filename, session=session)
            out_file_path = f"../twitter-flask/app/medias/{api_key}_{media_file.filename}"

            save_image(out_file_path, file=media_file)

            return {"result": True, "media_id": image_id}

        return {"result": True, "media_id": image.id}

