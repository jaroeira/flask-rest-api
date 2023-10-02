import pytest
from app.models import UserModel, TagModel
from app.services import article_service


def test_create_article_success(mock_get_sqlalchemy, mocker, app):
    """
    GIVEN: A article_data dict
    WHEN: calling article_service.create_article, a user is found and no arcle with the same name is found
    THEN: Shoud create an article
    """

    article_data = {
        "title": "Test title",
        "description": "test description",
        "content": "test content",
        "tags": ["tag1"]
    }

    user_id = "some-user-id"

    mock_user = UserModel(
        id=1,
        public_id=user_id,
        email="mock@test.com",
        username="mock",
        password="12345"
    )

    mock_get_sqlalchemy.filter_by.return_value.first.side_effect = [
        mock_user, None]

    mocker.patch('app.services.article_service._get_tags_to_add').return_value = [
        TagModel(id=1, name="tag1")]
    mocker.patch('app.utils.db_utils.save_db_item')
    save_db_item_spy = mocker.spy(article_service, 'save_db_item')

    with app.app_context():
        result = article_service.create_article(user_id, article_data)

    assert result[0]["message"] == "Article created!"
    assert result[0]["slug"] == "test-title"
    assert save_db_item_spy.call_count == 1
    assert result[1] == 201
