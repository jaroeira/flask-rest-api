from flask.views import MethodView
from flask_smorest import Blueprint
from app.dtos import CreateUserDto, FullUserToReturnDto, UpdateUserDto
import app.services.user_service as user_service

blp = Blueprint("User", "user", description="User api endpoints", url_prefix="/user")

@blp.route("/signup")
class UserSignup(MethodView):

    def post(self):
        return {"message": "user signup endpoint - TODO"}, 201
    
@blp.route("/verify-email")
class UserVerifyEmail(MethodView):

    def get(self):
        return {"message": "user verify email endpoint - TODO"}, 200


@blp.route("/signin")
class UserSignin(MethodView):

    def post(self):
        return {"message": "user signin endpoint - TODO"}, 200
    

@blp.route("/refresh-token")
class UserRefreshToken(MethodView):

    def post(self):
        return {"message": "user refresh token endpoint - TODO"}, 200
    

@blp.route("/revoke-refresh-token")
class UserRevokeRefreshToken(MethodView):

    def post(self):
        return {"message": "user revoke refresh token endpoint - TODO"}, 200
    
@blp.route("/forgot-password")
class UserForgotPassword(MethodView):

    def post(self):
        return {"message": "user forgot password endpoint - TODO"}, 200
    
@blp.route("/reset-password")
class UserResetPassword(MethodView):

    def post(self):
        return {"message": "user reset password endpoint - TODO"}, 200
    
@blp.route("/change-password")
class UserChangePassword(MethodView):

    def put(self):
        return {"message": "user change password endpoint - TODO"}, 200
    


# Admin only endpoints

@blp.route("/")
class User(MethodView):

    @blp.response(200, FullUserToReturnDto(many=True))
    def get(self):
        """Get a list of all users - Admin only"""
        return user_service.get_all_users()

    @blp.arguments(CreateUserDto)
    def post(self, user_data):
        """Create user - Admin only"""
        return user_service.create_user(user_data)
       
    @blp.arguments(UpdateUserDto)
    def put(self, user_data):
        """Update user - Admin only"""
        return user_service.update_user(user_data)
    

@blp.route("/<string:public_id>")
class UserById(MethodView):

    @blp.response(200, FullUserToReturnDto)
    def get(self, public_id):
        """Get a user by id - Admin only"""
        return user_service.get_user_by_id(public_id)
    
    def delete(self, public_id):
        """Delete a user by id - Admin only"""
        return user_service.remove_user_by_id(public_id)