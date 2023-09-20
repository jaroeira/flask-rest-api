from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import get_config
from .controllers.user import blp as UserBlueprint
from .controllers.auth import blp as AuthBlueprint
from .db import db


def create_app(env_name=None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(get_config(env_name))

    db.init_app(app)

    api = Api(app)

    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(AuthBlueprint)

    return app
