from typing import Any, Dict, List
from flask_smorest import abort
from app.models import ArticleModel, UserModel
from app.models import TagModel
from app.db import db
from datetime import datetime
from app.utils import save_db_item, delete_db_item

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

def get_all_articles():
    return ArticleModel.query.all()

def update_article(user_id, user_role, article_data):
    slug = article_data['slug']
   
    article: ArticleModel = ArticleModel.query.filter_by(_slug=slug).first_or_404(description='Article not found.')

    _check_authorization(article, user_id, user_role)

    article.title = article_data['title']
    article.description = article_data['description']
    article.content = article_data['content']
    article.updated_at = datetime.now()

    tagsToUpdate = article_data['tags']

    if(len(tagsToUpdate) > 0):
        tagsToUpdate = _get_tags_to_add(tagsToUpdate)

    article.tags = tagsToUpdate

    save_db_item(article, db)

    return {"message": "article successfully updated!"}, 200
  

def delete_article(user_id: str, user_role: str, slug: str):
     article: ArticleModel = ArticleModel.query.filter_by(_slug=slug).first_or_404(description='Article not found.')

     _check_authorization(article, user_id, user_role)

     delete_db_item(article, db)

     return {"message": "article successfully deleted!"}, 200


def _get_tags_to_add(tags: List[str]) -> List[TagModel]:
    existendTags = TagModel.query.filter(TagModel.name.in_(tags)).all()
    nonExistendTags = [TagModel(name=t) for t in tags if t not in [t.name for t in existendTags]]
    tagsToAdd = []
    tagsToAdd.extend(existendTags)
    tagsToAdd.extend(nonExistendTags)
    return tagsToAdd

def _check_authorization(article: ArticleModel, user_id: str, user_role: str):
    if not user_role == 'admin' and article.created_by.public_id != user_id:
        abort(403, message="Not authorized")