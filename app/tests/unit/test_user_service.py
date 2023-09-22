from app.services import user_service
from app.models import UserModel
from unittest.mock import Mock
import pytest
from werkzeug.exceptions import NotFound


user_to_return = UserModel(
    public_id="e512b548-a054-4eb1-9a9e-048405de6969",
    email="test@test.com",
    username="test",
    role="user",
    password="12345",
    email_verified=True
)


def test_get_user_by_success(monkeypatch, app):
    with app.app_context():
        user_model_mock = Mock()
        user_model_mock.filter_by.return_value.first.return_value = user_to_return
        monkeypatch.setattr(user_service.UserModel, 'query', user_model_mock)

        # Call the function
        result = user_service.get_user_by_id('valid_public_id')

        assert result == user_to_return


def test_get_user_by_fail(monkeypatch, app):
    with app.app_context():
        user_model_mock = Mock()
        user_model_mock.filter_by.return_value.first.return_value = None
        monkeypatch.setattr(user_service.UserModel, 'query', user_model_mock)

        # Call the function
        with pytest.raises(NotFound, match="404"):
            user_service.get_user_by_id('invalid_public_id')
