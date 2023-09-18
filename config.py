import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    API_TITLE = "Flask Rest API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_DEV_URL") or "sqlite:///dev_data.db"


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL")

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_PROD_URL")


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig,
    test=TestingConfig
)


def get_env() -> str:
    if os.environ.get("ENV") and os.environ.get("ENV") in config_by_name:
        return os.environ.get("ENV")
    else:
        return 'dev'


def get_config():
    return config_by_name[get_env()]
