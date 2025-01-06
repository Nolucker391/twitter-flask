import os

from flask import request
from flask_restx import Resource
from sqlalchemy import select, insert


from app.src.routes.FlaskAppSubSettings import api, app
from app.src.database.models import ApiKey, Session, User, Image

# UPLOAD_FOLDER = "../src/app/medias"
# UPLOAD_FOLDER = os.path.join(app.root_path, '..', 'app', 'medias')
ALLOWED_EXTENSIONS = ["gif", "jpg", "jpeg", "png"]


def get_image(filename, session):
    # query = session.execute(select(Image)).where(Image.filename == filename)
    # image = query.scalars().one_or_none()
    # return image
    query = select(Image).where(Image.filename == filename)
    result = session.execute(query).scalar_one_or_none()
    return result

def add_image_on_database(filename, session):
    print(f"Its add image : {filename}") # test_1000_F_225723068_Lajo41fOoMCeG2o2Ffe4rMng92rJB4LM.jpg
    # query = session.execute(insert(Image)).values(filename=filename).returning(Image.id)
    # session.commit()
    # image_id = query.scalar_one()
    # return image_id
    query = insert(Image).values(filename=filename).returning(Image.id)
    result = session.execute(query)
    session.commit()
    image_id = result.scalar_one()

    return image_id

def save_image(out_file_path, file):
    os.makedirs(os.path.dirname(out_file_path), exist_ok=True)
    filename = file.filename.replace('/', '_')
    file_path = os.path.join(out_file_path, filename)
    print(f"Saving file to: {file_path}")  # Добавьте отладочный вывод

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True) # Создаём директорию, если её нет
        if not os.path.exists(out_file_path):
            print(f"Directory {out_file_path} does not exist!")

        file.save(file_path)
        print(f"File saved successfully: {file_path}")
        return True
    except Exception as e:
        print(f"Error saving file: {str(e)}")
        return False


@api.route("/api/medias")
class MediaUploadResource(Resource):
    @api.doc(description="Load media files")
    def post(self):
        """
        Load media files
        """
        api_key = request.headers.get("api-key")
        session = Session()
        # query = session.query(User).join(ApiKey).filter(ApiKey.api_key == api_key).first()
        media_file = request.files["file"]
        filename = f"{api_key}_{media_file.filename}"

        image = get_image(filename=filename, session=session)
        print(f"mediafile: {media_file}\nfilename: {filename}")
        if not image:
            image_id = add_image_on_database(filename=filename, session=session)
            # out_file_path = f"../src/app/medias/{api_key}_{media_file.filename}"
            # out_file_path = f"../twitter-flask/app/medias/{api_key}_{media_file.filename}"

            out_file_path = os.path.join(app.root_path, 'medias', api_key)

            save_image(out_file_path, file=media_file)

            return {"result": True, "media_id": image_id}

        return {"result": True, "media_id": image.id}

