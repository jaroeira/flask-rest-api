from app.db import db
from sqlalchemy.sql import func
from slugify import slugify



class ArticleModel(db.Model):
    """ User Model for storing Article data"""
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _title = db.Column('title',db.String(200), nullable=False, unique=True)
    _slug = db.Column('slug',db.String(255), nullable=False, unique=True)
    description = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, default=func.now())
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    created_by_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_by = db.relationship(
        'UserModel', back_populates="articles")

    tags = db.relationship(
        'TagModel', secondary='article_tags')
    
    @property
    def slug(self):
        return self._slug
    
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self._slug = slugify(value)

    # @property
    # def like_count(self) -> int:
    #     return 1
    def __repr__(self):
        return f"<Article {self.title} - '{self.slug}'>"
