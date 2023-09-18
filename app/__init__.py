from flask import Flask
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from config import get_config
from .controllers.user import blp as UserBlueprint 


db = SQLAlchemy()

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(get_config())

    db.init_app(app)

    api = Api(app)

    api.register_blueprint(UserBlueprint)

    return app
