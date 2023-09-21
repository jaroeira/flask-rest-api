
from typing import List
from flask.testing import FlaskClient


def test_create_user(client: FlaskClient, populate_user_data):
    with client:
        # sigin as admin user
        client.post('/auth/signin',
                    json={"username": "test3", "password": "12345"})

        client.post('/auth/signin',
                    json={"username": "test3", "password": "12345"})
        res = client.post('/user/', json={
            "email": "create@test.com",
            "username": "Create",
            "role": "user",
            "password": "12345"
        })
        assert res.status_code == 201
        assert b"User created successfully!" in res.data
        public_id = res.json["public_id"]
        res_get_user = client.get(f'/user/{public_id}')
        assert public_id == res_get_user.json['public_id']
        assert res_get_user.json['email'] == "create@test.com"


def test_get_all_users(client: FlaskClient, populate_user_data):
    with client:
        # sigin as admin user
        client.post('/auth/signin',
                    json={"username": "test3", "password": "12345"})

        res = client.get('/user/')
        assert res.status_code == 200
        assert len(res.json) == 3


def test_get_user_by_id(client: FlaskClient, populate_user_data):
    with client:
        # sigin as admin user
        client.post('/auth/signin',
                    json={"username": "test3", "password": "12345"})

        public_id = "e512b548-a054-4eb1-9a9e-048405de6969"
        res = client.get(f'/user/{public_id}')
        assert res.status_code == 200
        assert res.json["public_id"] == public_id
