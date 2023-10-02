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
    THEN: Shoud have success with a http code 201
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
    THEN: Shoud have success with a http code 200
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
def test_get_articles_200(client: FlaskClient):
    """
    GIVEN: A unauthenticated request to GET /articles
    WHEN: passing pagination params
    THEN: Shoud have success with a http code 200 and receive a paginated response
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


@pytest.mark.filterwarnings("ignore:item_count")
@pytest.mark.usefixtures("populate_test_data")
def test_get_article_by_tag_200(client: FlaskClient):
    """
    GIVEN: A unauthenticated request to GET /articles filtered by teg
    WHEN: passing a tag
    THEN: Shoud have success with a http code 200 and a list of articles containg the tag name as filtered 
    """

    tag = 'tag3'

    res = client.get(f'articles/by-tag/{tag}')

    assert res.status_code == 200
    assert len(res.json["data"]) == 1
    assert tag in [tag['name'] for tag in res.json["data"][0]["tags"]]


@pytest.mark.filterwarnings("ignore:item_count")
@pytest.mark.usefixtures("populate_test_data")
def test_get_article_by_term_200(client: FlaskClient):
    """
    GIVEN: A unauthenticated request to GET /articles filterd by search term
    WHEN: passing a term as param
    THEN: Shoud have success with a http code 200 and receive a list of articles containing the term
    """

    search_term = 'editor'

    res = client.get(f'articles/by-term?term={search_term}')

    assert res.status_code == 200
    assert b"editor" in res.data


@pytest.mark.usefixtures("populate_test_data")
def test_article_like(client: FlaskClient):
    # sigin as user
    with client:
        client.post('/auth/signin',
                    json={"username": "test", "password": "12345"})

    slug = 'test-article'

    res = client.post(f'/articles/like/{slug}')
    assert res.status_code == 200
    assert b"Like added!" in res.data

    res = client.post(f'/articles/like/{slug}')
    assert res.status_code == 200
    assert b"Like removed!" in res.data


@pytest.mark.usefixtures("populate_test_data")
def test_delete_article_200(client: FlaskClient):
    """
    GIVEN: A authenticated request who created the article or has a admin role
    WHEN: passing slug as param of a existend article
    THEN: Shoud have success with a http code 200 and receive a delete confirmation message
    """

    # sigin as admin user
    with client:
        client.post('/auth/signin',
                    json={"username": "test3", "password": "12345"})

    slug = 'test-article'

    res = client.get(f'/articles/{slug}')
    assert res.status_code == 200

    res = client.delete(f'/articles/{slug}')
    assert res.status_code == 200
    assert b"article successfully deleted" in res.data

    res = client.get(f'/articles/{slug}')
    assert res.status_code == 404


@pytest.mark.usefixtures("populate_test_data")
def test_delete_article_404(client: FlaskClient):
    """
    GIVEN: A authenticated request who created the article or has a admin role
    WHEN: passing slug as param of a non existend article
    THEN: Shoud fail with a http code 404 
    """

    # sigin as admin user
    with client:
        client.post('/auth/signin',
                    json={"username": "test3", "password": "12345"})

    slug = 'non-existend-slug'
    res = client.delete(f'/articles/{slug}')
    assert res.status_code == 404


@pytest.mark.usefixtures("populate_test_data")
def test_delete_article_unauthenticated(client: FlaskClient):
    """
    GIVEN: A unauthenticated request
    WHEN: trying to delete an article
    THEN: Shoud fail with a http code 401
    """
    slug = 'test-article'
    res = client.delete(f'/articles/{slug}')
    assert res.status_code == 401


@pytest.mark.usefixtures("populate_test_data")
def test_delete_article_not_authorized(client: FlaskClient):
    """
    GIVEN: A authenticated request which has the role editor 
    WHEN: trying to delete an article created by another user
    THEN: Shoud fail with a http code 403
    """

    # sigin as user
    with client:
        client.post('/auth/signin',
                    json={"username": "test", "password": "12345"})

    slug = 'test-article'
    res = client.delete(f'/articles/{slug}')
    assert res.status_code == 403


@pytest.mark.usefixtures("populate_test_data")
def test_delete_editor_role_required(client: FlaskClient):
    """
    GIVEN: A authenticated request which has the role user 
    WHEN: trying to delete an article 
    THEN: Shoud fail with a http code 403
    """
    # sigin as user
    with client:
        client.post('/auth/signin',
                    json={"username": "simple-user", "password": "12345"})
    slug = 'test-article'
    res = client.delete(f'/articles/{slug}')
    assert res.status_code == 403
    assert b"editors only" in res.data
