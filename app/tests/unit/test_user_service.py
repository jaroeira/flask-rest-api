from app.services import user_service
from app.models import UserModel
import pytest
from werkzeug.exceptions import NotFound, Conflict


def test_get_user_by_id_success(mock_get_sqlalchemy, user_mock_model):
    """
    GIVEN: A valid user public_ic
    WHEN: calling user_service.get_user_by_id('valid_public_id')
    THEN: Shoud return an user object
    """
    mock_get_sqlalchemy.filter_by.return_value.first.return_value = user_mock_model
    # Call the function
    result = user_service.get_user_by_id('valid_public_id')
    assert result == user_mock_model


def test_get_user_by_id_fail(mock_get_sqlalchemy):
    """
    GIVEN: A invalid user public_ic
    WHEN: calling user_service.get_user_by_id('valid_public_id')
    THEN: Shoud raise an error 404
    """

    mock_get_sqlalchemy.filter_by.return_value.first.return_value = None

    # Call the function
    with pytest.raises(NotFound, match="404"):
        user_service.get_user_by_id('invalid_public_id')


def test_get_all_users(mock_get_sqlalchemy, user_mock_model):
    """
    WHEN: calling user_service.get_all_users()
    THEN: Shoud return a list of users
    """

    mock_get_sqlalchemy.all.return_value = [user_mock_model]
    result = user_service.get_all_users()
    assert result == [user_mock_model]


def test_create_user_success(mock_get_sqlalchemy, mocker, app):
    """
    GIVEN: A user_data dict
    WHEN: calling user_service.create_user(user_data) and username are not in use
    THEN: Shoud create an user with the dict data
    """

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


def test_create_user_fail(mock_get_sqlalchemy, user_mock_model, app):
    """
    GIVEN: A user_data dict
    WHEN: calling user_service.create_user(user_data) and username are already in use
    THEN: Shoud raise an error 409
    """

    user_data = {
        "email": "create_test@test.com",
        "username": "create_test",
        "password": "12345"
    }
    mock_get_sqlalchemy.filter.return_value.first.return_value = user_mock_model

    with app.app_context():
        with pytest.raises(Conflict, match="409"):
            user_service.create_user(user_data)


def test_update_user_not_found_fail(mock_get_sqlalchemy):
    """
    GIVEN: A user_data dict
    WHEN:  calling user_service.uptate_user(user_data) and user is not found
    THEN:  Shoud raise an error 404
    """
    mock_get_sqlalchemy.filter_by.return_value.first.return_value = None

    user_data = {
        "public_id": "not_found",
        "email": "not_foundt@test.com",
        "username": "not_found",
    }

    with pytest.raises(NotFound, match="404"):
        user_service.update_user(user_data)


def test_update_user_email_in_use_fail(mock_get_sqlalchemy, user_mock_model, mocker):
    """
    GIVEN: A user_data dict
    WHEN:  calling user_service.uptate_user(user_data) and new email is already in use
    THEN:  Shoud raise an error 404
    """

    #
    mock_get_sqlalchemy.filter_by.return_value.first.return_value = user_mock_model
    mocker.patch(
        "app.services.user_service._check_if_email_exists").return_value = True

    user_data = {
        "public_id": "some_id",
        "email": "new_email@test.com",
        "username": "older_name",
    }

    with pytest.raises(Conflict, match="409"):
        user_service.update_user(user_data)


def test_update_user_username_in_use_fail(mock_get_sqlalchemy, user_mock_model, mocker):
    """
    GIVEN: A user_data dict
    WHEN:  calling user_service.uptate_user(user_data) and new username is already in use
    THEN:  Shoud raise an error 404
    """
    mock_get_sqlalchemy.filter_by.return_value.first.return_value = user_mock_model
    mocker.patch(
        "app.services.user_service._check_if_email_exists").return_value = False

    mocker.patch(
        "app.services.user_service._check_if_username_exists").return_value = True

    user_data = {
        "public_id": "some_id",
        "email": "new_email@test.com",
        "username": "new_name",
    }

    with pytest.raises(Conflict, match="409"):
        user_service.update_user(user_data)


def test_update_user_success(mock_get_sqlalchemy, user_mock_model, mocker, app):
    """
    GIVEN: A user_data dict
    WHEN:  calling user_service.uptate_user(user_data) 
    THEN:  Shoud have success http 200
    """

    user_data = {
        "public_id": "some_id",
        "email": "new_email@test.com",
        "username": "new_name",
        "role": "Admin",
        "email_verified": False
    }

    mock_get_sqlalchemy.filter_by.return_value.first.return_value = user_mock_model
    mocker.patch(
        "app.services.user_service._check_if_email_exists").return_value = False
    mocker.patch(
        "app.services.user_service._check_if_username_exists").return_value = False
    mocker.patch('app.services.user_service.save_db_item')
    save_db_item_spy = mocker.spy(user_service, 'save_db_item')

    with app.app_context():
        result = user_service.update_user(user_data)
        assert result[1] == 200

        assert save_db_item_spy.call_count == 1
        updated_user: UserModel = save_db_item_spy.call_args[0][0]
        assert updated_user.email == user_data["email"]
        assert updated_user.username == user_data["username"]
        assert updated_user.role == "admin"
        assert updated_user.email_verified == user_data["email_verified"]


def test_remove_user_by_id_not_found_fail(mock_get_sqlalchemy):
    """
    GIVEN: A user public_id
    WHEN:  calling user_service.remove_user_by_id(public_id: str) and user is not found
    THEN:  Shoud raise error 404
    """

    mock_get_sqlalchemy.filter_by.return_value.first.return_value = None

    # Call the function
    with pytest.raises(NotFound, match="404"):
        user_service.remove_user_by_id('invalid_public_id')


def test_remove_user_by_id_success(mock_get_sqlalchemy, user_mock_model, mocker, app):
    """
    GIVEN: A user public_id
    WHEN:  calling user_service.remove_user_by_id(public_id: str) 
    THEN:  Shoud have success
    """

    mock_get_sqlalchemy.filter_by.return_value.first.return_value = user_mock_model
    mocker.patch('app.services.user_service.delete_db_item')
    delete_db_item_spy = mocker.spy(user_service, 'delete_db_item')

    with app.app_context():
        result = user_service.remove_user_by_id('valid_id')
        assert result[1] == 200
        assert delete_db_item_spy.call_count == 1
        assert delete_db_item_spy.call_args[0][0] == user_mock_model
