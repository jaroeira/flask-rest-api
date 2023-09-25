from app.db import db


class ArticleTagsModel(db.Model):
    __tablename__ = "article_tags"

    article_id = db.Column(db.Integer, db.ForeignKey(
        'articles.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey(
        'tags.id'), primary_key=True)
