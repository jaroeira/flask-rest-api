from flask.views import MethodView
from flask_smorest import Blueprint
from app.dtos import UserDto, SigninUserDto
import app.services.user_service as user_service
import app.services.auth_service as auth_service

blp = Blueprint(
    "Auth", "auth", description="Authentication api endpoints", url_prefix="/auth")


@blp.route("/signup")
class UserSignup(MethodView):

    @blp.arguments(UserDto)
    def post(self, user_data):
        """Signup User -> create an user with role user"""
        return user_service.create_user(user_data)


@blp.route("/verify-email")
class UserVerifyEmail(MethodView):

    def get(self):
        return {"message": "user verify email endpoint - TODO"}, 200


@blp.route("/signin")
class UserSignin(MethodView):

    @blp.arguments(SigninUserDto)
    def post(self, user_data):
       return auth_service.signin_user(user_data)

  


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