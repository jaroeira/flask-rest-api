import json
import pytest
from app import create_app
from app.db import db
from app.models import UserModel
import os


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


@pytest.fixture
def populate_user_data(app):
    with app.app_context():
        data_file_path = os.path.join(os.path.dirname(
            __file__), "data", "users_test_data.json")

        with open(data_file_path, "r") as json_file:
            data = json.load(json_file)
            for item in data:
                user = UserModel(**item)
                db.session.add(user)
            db.session.commit()
