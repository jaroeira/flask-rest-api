import json
from flask.testing import FlaskClient
import pytest
import os
import math


@pytest.mark.usefixtures("populate_test_data")
def test_create_article_success(client: FlaskClient):
    """
    GIVEN: A logged user with a editor role
    WHEN: creating a new article
    THEN: Shoud success with a http code 201
    """

    with client:
        # sigin as editor user
        client.post('/auth/signin',
                    json={"username": "test", "password": "12345"})
        res = client.post('/articles/', json={
            "title": "Article Test",
            "description": "Article description test",
            "content": "Article test content .......",
            "tags": ["tag1", "TAG4"]
        })

        assert res.status_code == 201


@pytest.mark.usefixtures("populate_test_data")
def test_create_article_401(client: FlaskClient):
    """
    GIVEN: A logged user with a normal user role
    WHEN: creating a new article
    THEN: Shoud fail with a http code 401
    """

    with client:
        # signin as normal user
        client.post('/auth/signin',
                    json={"username": "verification-token", "password": "12345"})
        res = client.post('/articles/', json={
            "title": "Article Test",
            "description": "Article description test",
            "content": "Article test content .......",
            "tags": ["tag1", "TAG4"]
        })

        assert res.status_code == 401


@pytest.mark.usefixtures("populate_test_data")
def test_update_article_401(client: FlaskClient):
    """
    GIVEN: A logged user with editor role
    WHEN: updates an article created by another user
    THEN: Shoud fail with a http code 403
    """

    with client:
        # signin as editor user
        client.post('/auth/signin',
                    json={"username": "test", "password": "12345"})

        res = client.put('/articles/', json={
            "title": "Test Article",
            "slug": "test-article",
            "description": "test description updated!",
            "content": "test content",
            "tags": ["tag1"]
        })

        assert res.status_code == 403


@pytest.mark.usefixtures("populate_test_data")
def test_update_article_200(client: FlaskClient):
    """
    GIVEN: A logged user with editor role
    WHEN: updates an article created by himself 
    THEN: Shoud success with a http code 200
    """

    with client:
        # signin as editor user
        client.post('/auth/signin',
                    json={"username": "test", "password": "12345"})

        res = client.put('/articles/', json={
            "title": "Test Article Editor",
            "slug": "test-article-editor",
            "description": "test description updated!",
            "content": "test content",
            "tags": ["tag3"]
        })

        assert res.status_code == 200


@pytest.mark.filterwarnings("ignore:item_count")
@pytest.mark.usefixtures("populate_test_data")
def test_get_article_200(client: FlaskClient):
    """
    GIVEN: A unauthenticated request to GET /articles
    WHEN: passing pagination params
    THEN: Shoud success with a http code 200 and receibe a paginated response
    """

    page_size = 1
    page = 1

    res = client.get(f'/articles/?page={page}&page_size={page_size}')

    assert res.status_code == 200
    assert res.json["page_size"] == page_size
    assert res.json["page"] == page

    article_data_file_path = os.path.join(os.path.dirname(
        __file__), "..", "data", "articles_test_data.json")

    with open(article_data_file_path, "r") as json_file:
        data = json.load(json_file)
        total_items = len(data)

        assert res.json["total_items"] == total_items
        assert res.json["total_pages"] == math.ceil(total_items / page_size)

    print(res.json["data"][0]['tags'])
