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
    assert res.json["access_token"] != None
     
