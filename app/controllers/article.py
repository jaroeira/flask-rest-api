from flask.views import MethodView
from flask_smorest import Blueprint
from app.dtos import ArticleToInsertDto, ArticleToReturnDto, ArticleToUpdateDto
import app.services.article_service as article_service
blp = Blueprint(
    "Article", "article", description="Articles api endpoints", url_prefix="/articles")

@blp.route("/")
class User(MethodView):

    @blp.arguments(ArticleToInsertDto)
    def post(self, article_data):
        return article_service.create_article(article_data)
    
    @blp.response(200, ArticleToReturnDto(many=True))
    def get(self):
        return article_service.get_all_articles()
    
    @blp.arguments(ArticleToUpdateDto)
    def put(self, article_data):
        return article_service.update_article(article_data)
    

@blp.route("/<string:slug>")
class User(MethodView):

    def delete(self, slug):
        return article_service.delete_article(slug)
   
     