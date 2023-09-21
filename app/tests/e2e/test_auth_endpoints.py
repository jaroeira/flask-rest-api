from flask.testing import FlaskClient


def test_sigup_user(client: FlaskClient):
    res = client.post('/auth/signup', json={
        "username": "signup",
        "email": "signup@test.com",
        "password": "12345"
    })

    assert res.status_code == 201
    assert b"User created successfully!" in res.data


def test_signin_incorrect_passord(client: FlaskClient, populate_user_data):
    res = client.post('/auth/signin', json={
        "username": "test",
        "password": "incorrect_password"
    })

    assert res.status_code == 401


def test_signin_incorrect_username(client: FlaskClient, populate_user_data):
    res = client.post('/auth/signin', json={
        "username": "incorrect_username",
        "password": "12345"
    })

    assert res.status_code == 401


def test_sigin_success(client: FlaskClient, populate_user_data):
    res = client.post('/auth/signin', json={
        "username": "test",
        "password": "12345"
    })

    assert res.status_code == 200


def test_verify_email_success(client: FlaskClient, populate_user_data):
    res = client.get('/auth/verify-email?token=9bb9a1860a6408de7107ec991ec320f5faec9ae019c1ba64409159d7ce7f85cb', json={
        "username": "verification-token",
        "password": "12345"
    })

    assert res.status_code == 200
    assert b"email address was successfully verified" in res.data


def test_verify_email_fail(client: FlaskClient, populate_user_data):
    res = client.get('/auth/verify-email?token=abcd', json={
        "username": "verification-token",
        "password": "12345"
    })

    assert res.status_code == 403
