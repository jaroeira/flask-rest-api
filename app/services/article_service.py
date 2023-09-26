from typing import Any, Dict, List
from app.models import ArticleModel, UserModel
from app.models import TagModel
from app.db import db
from datetime import datetime

def create_article(user_id: str, article_data: Dict[str, Any]):

    article = ArticleModel(
        title=article_data["title"],
        description=article_data["description"],
        content=article_data["content"],
        created_by_id=user_id
    )

    tagsToAdd = _get_tags_to_add(article_data["tags"])

    article.tags = tagsToAdd

    db.session.add(article)
    db.session.commit()

    return {"message": "ok"}, 200

def get_all_articles():
    return ArticleModel.query.all()

def update_article(article_data):
    slug = article_data['slug']
   
    article: ArticleModel = ArticleModel.query.filter_by(_slug=slug).first_or_404(description='Article not found.')

    article.title = article_data['title']
    article.description = article_data['description']
    article.content = article_data['content']
    article.updated_at = datetime.now()

    tagsToUpdate = article_data['tags']

    if(len(tagsToUpdate) > 0):
        tagsToUpdate = _get_tags_to_add(tagsToUpdate)

    article.tags = tagsToUpdate

    db.session.add(article)
    db.session.commit()


    return {"message": "article successfully updated!"}, 200
  

def delete_article(slug: str):
     article: ArticleModel = ArticleModel.query.filter_by(_slug=slug).first_or_404(description='Article not found.')

     db.session.delete(article)
     db.session.commit()

     return {"message": "article successfully deleted!"}, 200


def _get_tags_to_add(tags: List[str]) -> List[TagModel]:
    existendTags = TagModel.query.filter(TagModel.name.in_(tags)).all()
    nonExistendTags = [TagModel(name=t) for t in tags if t not in [t.name for t in existendTags]]
    tagsToAdd = []
    tagsToAdd.extend(existendTags)
    tagsToAdd.extend(nonExistendTags)
    return tagsToAdd
