from typing import Any, Dict, List
from flask import url_for
from flask_smorest import abort
from sqlalchemy import desc, or_
from flask_sqlalchemy.query import Query
from app.models import ArticleModel, UserModel, ArticleLikesModel, ArticleImageModel
from app.models import TagModel
from app.db import db
from datetime import datetime
from app.utils import save_db_item, delete_db_item, save_image, delete_file



def create_article(user_id: str, article_data: Dict[str, Any]):

    user: UserModel = UserModel.query.filter_by(public_id=user_id).first()

    article = ArticleModel(
        title=article_data["title"],
        description=article_data["description"],
        content=article_data["content"],
        created_by_id=user.id
    )

    tagsToAdd = _get_tags_to_add(article_data["tags"])

    article.tags = tagsToAdd

    save_db_item(article, db)

    return {"message": "Article created!", "slug": article.slug}, 201


def get_all_articles(pagination_parameters):
    return _paginate_response(ArticleModel.query.order_by(
        desc(ArticleModel.id)), pagination_parameters)


def get_articles_by_tag(tag, pagination_parameters):
    query = ArticleModel.query.join(ArticleModel.tags).filter(
        TagModel.name == tag).order_by(desc(ArticleModel.id))
    return _paginate_response(query, pagination_parameters)


def get_articles_by_search_term(search_term, pagination_parameters):

    term = search_term['term']

    query = ArticleModel.query.filter(or_(ArticleModel.description.ilike(
        f'%{term}%'), ArticleModel.content.ilike(f'%{term}%'))).order_by(desc(ArticleModel.id))

    return _paginate_response(query, pagination_parameters)


def get_article_by_slug(slug: str):
    article = ArticleModel.query.filter_by(_slug=slug).first_or_404()
    return article


def update_article(user_id, user_role, article_data):
    slug = article_data['slug']

    article: ArticleModel = ArticleModel.query.filter_by(
        _slug=slug).first_or_404(description='Article not found.')

    _check_authorization(article, user_id, user_role)

    article.title = article_data['title']
    article.description = article_data['description']
    article.content = article_data['content']
    article.updated_at = datetime.now()

    tagsToUpdate = article_data['tags']

    if (len(tagsToUpdate) > 0):
        tagsToUpdate = _get_tags_to_add(tagsToUpdate)

    article.tags = tagsToUpdate

    save_db_item(article, db)

    return {"message": "article successfully updated!"}, 200


def delete_article(user_id: str, user_role: str, slug: str):
    article: ArticleModel = ArticleModel.query.filter_by(
        _slug=slug).first_or_404(description='Article not found.')

    _check_authorization(article, user_id, user_role)

    images: list[ArticleImageModel] = article.images
    image_urls = [url.image_url for url in images]

    delete_db_item(article, db)

    for url in image_urls:
        delete_file(url)

    return {"message": "article successfully deleted!"}, 200


def like_article(user_id: str, slug: str):
    article: ArticleModel = ArticleModel.query.filter_by(
        _slug=slug).first_or_404(description='Article not found.')
    user: UserModel = UserModel.query.filter_by(public_id=user_id).first()

    liked = ArticleLikesModel.query.filter_by(
        article_id=article.id, user_id=user.id).first()

    if not liked:
        like = ArticleLikesModel(
            article_id=article.id,
            user_id=user.id
        )
        save_db_item(like, db)
        return {"message": "Like added!"}, 200
    else:
        delete_db_item(liked, db)
        return {"message": "Like removed!"}, 200


def upload_image(image, slug):

    article: ArticleModel = ArticleModel.query.filter_by(
        _slug=slug).first()

    try:
        file_name = save_image(image)
        image_url = url_for('static', filename=f'uploads/{file_name}')

        article_image = ArticleImageModel(
            image_url=image_url,
            article=article
        )

        save_db_item(article_image, db)

        return {"message": "upload sucessfully uploaded!", "image url": image_url}
    except Exception as e:
        print(f"Error in save_image: {str(e)}")
        abort(500)


def _get_tags_to_add(tags: List[str]) -> List[TagModel]:
    existendTags = TagModel.query.filter(TagModel.name.in_(tags)).all()
    nonExistendTags = [TagModel(name=t) for t in tags if t not in [
        t.name for t in existendTags]]
    tagsToAdd = []
    tagsToAdd.extend(existendTags)
    tagsToAdd.extend(nonExistendTags)
    return tagsToAdd


def _check_authorization(article: ArticleModel, user_id: str, user_role: str):
    if not user_role == 'admin' and article.created_by.public_id != user_id:
        abort(403, message="Not authorized")


def _paginate_response(query: Query, pagination_parameters):
    page_size = pagination_parameters.page_size
    page = pagination_parameters.page

    result = query.paginate(page=page, per_page=page_size)

    return {
        "page_size": result.per_page,
        "page": result.page,
        "total_items": result.total,
        "total_pages": result.pages,
        "has_prev": result.has_prev,
        "has_next": result.has_next,
        "data": result.items
    }
