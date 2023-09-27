from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils import role_required, get_user_role, validate_image
from app.dtos import ArticleToInsertDto, PaginatedArticlesDto, ArticleToUpdateDto, ArticleSearchTerm, ArticleUploadImageDto
import app.services.article_service as article_service
blp = Blueprint(
    "Article", "article", description="Articles api endpoints", url_prefix="/articles")


@blp.route("/")
class Article(MethodView):

    @role_required('editor')
    @blp.arguments(ArticleToInsertDto)
    def post(self, article_data):
        user_id = get_jwt_identity()
        return article_service.create_article(user_id, article_data)

    @blp.paginate()
    @blp.response(200, PaginatedArticlesDto)
    def get(self, pagination_parameters):
        return article_service.get_all_articles(pagination_parameters)

    @role_required('editor')
    @blp.arguments(ArticleToUpdateDto)
    def put(self, article_data):
        user_id = get_jwt_identity()
        user_role = get_user_role()
        return article_service.update_article(user_id, user_role, article_data)


@blp.route("/<string:slug>")
class ArticleById(MethodView):

    @role_required('editor')
    def delete(self, slug):
        user_id = get_jwt_identity()
        user_role = get_user_role()
        return article_service.delete_article(user_id, user_role, slug)


@blp.route("/like/<string:slug>")
class ArticleLike(MethodView):

    @jwt_required()
    def post(self, slug):
        user_id = get_jwt_identity()
        return article_service.like_article(user_id, slug)


@blp.route("/by-tag/<string:tag>")
class ArticleByTag(MethodView):

    @blp.paginate()
    @blp.response(200, PaginatedArticlesDto)
    def get(self, tag, pagination_parameters):
        return article_service.get_articles_by_tag(tag, pagination_parameters)


@blp.route("/by-term")
class ArticleByTag(MethodView):

    @blp.paginate()
    @blp.arguments(ArticleSearchTerm, location="query")
    @blp.response(200, PaginatedArticlesDto)
    def get(self, search_term, pagination_parameters):
        return article_service.get_articles_by_search_term(search_term, pagination_parameters)


@blp.route("/<string:slug>/upload-image")
class ArticleUploadImage(MethodView):

    @blp.arguments(ArticleUploadImageDto, location="files")
    @validate_image()
    def post(self, files, slug):
        image = files['image']
        return article_service.upload_image(image, slug)
