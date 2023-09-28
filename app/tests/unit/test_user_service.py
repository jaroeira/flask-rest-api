from app.services import user_service
from app.models import UserModel
import pytest
from werkzeug.exceptions import NotFound


def test_get_user_by_id_success(mock_get_sqlalchemy, user_mock_model):
    mock_get_sqlalchemy.filter_by.return_value.first.return_value = user_mock_model
    # Call the function
    result = user_service.get_user_by_id('valid_public_id')
    assert result == user_mock_model


def test_get_user_by_id_fail(mock_get_sqlalchemy):
    mock_get_sqlalchemy.filter_by.return_value.first.return_value = None

    # Call the function
    with pytest.raises(NotFound, match="404"):
        user_service.get_user_by_id('invalid_public_id')


def test_get_all_users(mock_get_sqlalchemy, user_mock_model):
    mock_get_sqlalchemy.all.return_value = [user_mock_model]
    result = user_service.get_all_users()
    assert result == [user_mock_model]


def test_create_user(mock_get_sqlalchemy, mocker, app):
    mocker.patch('app.utils.db_utils.save_db_item')
    mock_get_sqlalchemy.filter.return_value.first.return_value = None
    mock_get_sqlalchemy.count.return_value = 1

    save_db_item_spy = mocker.spy(user_service, 'save_db_item')

    user_data = {
        "email": "create_test@test.com",
        "username": "create_test",
        "password": "12345"
    }

    with app.app_context():
        result = user_service.create_user(user_data)
        assert result[0]["message"] == "User created successfully!"
        assert save_db_item_spy.call_count == 1

        created_user = save_db_item_spy.call_args[0][0]
        assert created_user.email == 'create_test@test.com'
        assert created_user.username == 'create_test'
        assert created_user.password_hash != '12345'
        assert created_user.role == 'user'
        assert created_user.email_verified == False
