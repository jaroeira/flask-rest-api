from flask.views import MethodView
from flask_smorest import Blueprint
from app.dtos import CreateUserDto, FullUserToReturnDto, UpdateUserDto
from app.utils import role_required
import app.services.user_service as user_service

blp = Blueprint(
    "User", "user", description="User api endpoints", url_prefix="/user")


# Admin only endpoints

@blp.route("/")
class User(MethodView):


    @role_required('admin')
    @blp.response(200, FullUserToReturnDto(many=True))
    def get(self):
        """Get a list of all users - Admin only"""
        return user_service.get_all_users()

    @role_required('admin')
    @blp.arguments(CreateUserDto)
    def post(self, user_data):
        """Create user - Admin only"""
        return user_service.create_user(user_data)

    @role_required('admin')
    @blp.arguments(UpdateUserDto)
    def put(self, user_data):
        """Update user - Admin only"""
        return user_service.update_user(user_data)


@blp.route("/<string:public_id>")
class UserById(MethodView):

    @role_required('admin')
    @blp.response(200, FullUserToReturnDto)
    def get(self, public_id):
        """Get a user by id - Admin only"""
        return user_service.get_user_by_id(public_id)

    @role_required('admin')
    def delete(self, public_id):
        """Delete a user by id - Admin only"""
        return user_service.remove_user_by_id(public_id)
