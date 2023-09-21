from flask.views import MethodView
from flask_smorest import Blueprint
from app.dtos import UserDto, SigninUserDto, EmailVerificationTokenDto, ForgotPasswordDto, ResetPasswordDto
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

    @blp.arguments(EmailVerificationTokenDto, location='query')
    def get(self, params):
        return auth_service.verify_user_email(params['token'])


@blp.route("/signin")
class UserSignin(MethodView):

    @blp.arguments(SigninUserDto)
    def post(self, user_data):
        return auth_service.signin_user(user_data)


@blp.route("/forgot-password")
class UserForgotPassword(MethodView):

    @blp.arguments(ForgotPasswordDto)
    def post(self, params):
        email = params["email"]
        return auth_service.forgot_password(email)


@blp.route("/reset-password")
class UserResetPassword(MethodView):

    @blp.arguments(ResetPasswordDto)
    def post(self, params):
        reset_token = params["token"],
        new_password = params["new_password"]
        return auth_service.reset_password(reset_token, new_password)


@blp.route("/change-password")
class UserChangePassword(MethodView):

    def put(self):
        return {"message": "user change password endpoint - TODO"}, 200
