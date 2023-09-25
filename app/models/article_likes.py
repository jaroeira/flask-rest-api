from app.db import db


class ArticleLikesModel(db.Model):
    __tablename__ = "article_likes"

    article_id = db.Column(db.Integer, db.ForeignKey(
        'articles.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), primary_key=True)
