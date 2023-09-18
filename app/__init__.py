from flask import Flask
from flask_smorest import Api
from config import get_config
from .controllers.user import blp as UserBlueprint 


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(get_config())
    api = Api(app)

    api.register_blueprint(UserBlueprint)

    return app
