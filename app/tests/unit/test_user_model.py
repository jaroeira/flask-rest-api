from app.models import UserModel


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """

    email = "test@test.com",
    username = "Test",
    role = "user",
    password = "12345"

    new_user = UserModel(email=email, username=username,
                         role=role, password=password)
    assert new_user.email == email
    assert new_user.username == username
    assert new_user.role == role
    assert new_user.password_hash != password
