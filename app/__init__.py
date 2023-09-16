from flask import Flask
from config import get_config


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(get_config())

    return app
