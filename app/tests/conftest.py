import json
import pytest
from app import create_app
from app.db import db
from app.models import UserModel, ArticleModel
import os
from unittest.mock import Mock


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
def patch_emails_queue(monkeypatch, app):

    mock_enqueue = Mock()
    mock_enqueue.enqueue.return_value = None

    with app.app_context():
        emails_queue_mock = Mock()
        emails_queue_mock.return_value = None
        monkeypatch.setattr(app, 'emails_queue', mock_enqueue)


@pytest.fixture(autouse=True)
def populate_test_data(app):
    with app.app_context():
        user_data_file_path = os.path.join(os.path.dirname(
            __file__), "data", "users_test_data.json")

        with open(user_data_file_path, "r") as json_file:
            data = json.load(json_file)
            for item in data:
                user = UserModel(**item)
                db.session.add(user)
            db.session.commit()

        article_data_file_path = os.path.join(os.path.dirname(
            __file__), "data", "articles_test_data.json")

        with open(article_data_file_path, "r") as json_file:
            data = json.load(json_file)
            for item in data:
                article = ArticleModel(
                    title=item["title"],
                    description=item["description"],
                    content=item["content"],
                    created_by_id=item["created_by_id"]
                )
                db.session.add(article)
            db.session.commit()
