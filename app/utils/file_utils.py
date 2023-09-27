from functools import wraps
from werkzeug.datastructures import FileStorage
from flask import jsonify
from werkzeug.utils import secure_filename
import os
from uuid import uuid4

base_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..'))


def save_image(image: FileStorage):

    uploads_folder = 'uploads'

    file_extension = image.filename.lower().split(".")[-1]
    filename = secure_filename(image.filename)
    filename = f'{uuid4()}.{file_extension}'

    file_path = os.path.join(base_dir, "app", "static",
                             uploads_folder, filename)

    image.save(file_path)

    return filename


def validate_image():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            for arg in args:
                if isinstance(arg, dict) and "image" in arg:
                    image: FileStorage = arg["image"]

                    allowed_extensions = ["jpg", "jpeg", "png"]
                    max_file_size = 10 * 1024 * 1024  # 10 MB in bytes

                    file_extension = image.filename.lower().split(".")[-1]
                    image.stream.seek(0, 2)
                    file_size = image.stream.tell()
                    image.stream.seek(0)

                    if not file_extension in allowed_extensions:
                        return jsonify(message="Invalid file extension. Allowed extensions are .jpg, .jpeg, .png."), 400

                    if file_size > max_file_size:
                        return jsonify(message="File size exceeds 10 MB."), 400

            return fn(*args, **kwargs)
        return decorator

    return wrapper


def delete_file(file_path: str):

    full_file_path = os.path.join(
        base_dir, 'app', file_path.lstrip('/'))

    if os.path.exists(full_file_path):
        try:
            os.remove(full_file_path)
            print(f"File {file_path} deleted successfully.")
        except PermissionError:
            print(f"Permission denied: Unable to delete {full_file_path}.")
        except Exception as e:
            print(f"An error occurred while deleting {full_file_path}: {e}")
    else:
        print(f"File {full_file_path} does not exist.")
