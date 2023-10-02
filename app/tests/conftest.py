import json
import pytest
from app import create_app
from app.db import db
from app.models import UserModel, ArticleModel, TagModel, ArticleTagsModel
import os
from unittest.mock import Mock
import sqlite3


@pytest.fixture
def app():
    app = create_app("test")

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def patch_send_email(monkeypatch):
    # Define a mock implementation of send_email
    def mock_send_email(to, subject, body, html):
        # Mock implementation
        return {"status_code": 200, "message": "Email sent successfully"}

    monkeypatch.setattr('tasks.email_task.send_email', mock_send_email)


@pytest.fixture(autouse=True)
def patch_tasks_queue(monkeypatch, app):

    mock_enqueue = Mock()
    mock_enqueue.enqueue.return_value = None

    with app.app_context():
        emails_queue_mock = Mock()
        emails_queue_mock.return_value = None
        monkeypatch.setattr(app, 'tasks_queue', mock_enqueue)


@pytest.fixture()
def populate_test_data(app):
    with app.app_context():
        load_test_data_from_json(UserModel, "users_test_data.json")
        load_test_data_from_json(TagModel, "tags_test_data.json")
        load_test_data_from_json(ArticleModel, "articles_test_data.json")
        load_test_data_from_json(
            ArticleTagsModel, "article_tags_test_data.json")


@pytest.fixture
def mock_get_sqlalchemy(mocker):

    mock = mocker.patch(
        "flask_sqlalchemy.model._QueryProperty.__get__").return_value = mocker.Mock()
    return mock


@pytest.fixture
def user_mock_model():
    mock_model = UserModel(
        public_id="e512b548-a054-4eb1-9a9e-048405de6969",
        email="mock@test.com",
        username="mock",
        role="user",
        password="12345",
        email_verified=True
    )
    return mock_model


def load_test_data_from_json(model, json_file_name):

    file_path = os.path.join(os.path.dirname(
        __file__), "data", json_file_name)

    with open(file_path, "r") as json_file:
        json_data = json.load(json_file)

    columns_to_populate = list(json_data[0].keys())

    data_to_insert = [
        {col: item[col] for col in columns_to_populate}
        for item in json_data
    ]

    conn = db.engine.connect()
    transaction = conn.begin()

    try:
        conn.execute(model.__table__.insert().values(data_to_insert))
        transaction.commit()
    except:
        transaction.rollback()
        raise
    finally:
        conn.close()
