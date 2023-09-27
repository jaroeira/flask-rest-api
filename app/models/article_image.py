from app.db import db
from sqlalchemy.sql import func


class ArticleImageModel(db.Model):
    """ Article Image Model for storing Article images urls"""
    __tablename__ = "article_images"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_url = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())

    article_id = db.Column(db.Integer, db.ForeignKey(
        'articles.id'), nullable=False)

    article = db.relationship(
        'ArticleModel', back_populates='images')
