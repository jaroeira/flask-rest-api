from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate
from config import get_config
from .controllers.user import blp as UserBlueprint 
from .db import db



def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(get_config())

    db.init_app(app)

    api = Api(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(UserBlueprint)

    return app
