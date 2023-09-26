from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils import role_required, get_user_role
from app.dtos import ArticleToInsertDto, ArticleToReturnDto, ArticleToUpdateDto
import app.services.article_service as article_service
blp = Blueprint(
    "Article", "article", description="Articles api endpoints", url_prefix="/articles")

@blp.route("/")
class User(MethodView):

    @role_required('editor')
    @blp.arguments(ArticleToInsertDto)
    def post(self, article_data):
        user_id = get_jwt_identity()
        return article_service.create_article(user_id, article_data)
    
    @blp.response(200, ArticleToReturnDto(many=True))
    def get(self):
        return article_service.get_all_articles()
    
    @role_required('editor')
    @blp.arguments(ArticleToUpdateDto)
    def put(self, article_data):
        user_id = get_jwt_identity()
        user_role = get_user_role()
        return article_service.update_article(user_id, user_role, article_data)
    

@blp.route("/<string:slug>")
class User(MethodView):

    @role_required('editor')
    def delete(self, slug):
        user_id = get_jwt_identity()
        user_role = get_user_role()
        return article_service.delete_article(user_id, user_role, slug)
    

   
@blp.route("/like/<string:slug>")
class User(MethodView):

    @jwt_required()
    def post(self, slug):
        return {"message": "like article - TODO"}, 200
    