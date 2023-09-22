from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.dtos import UserDto, SigninUserDto, EmailVerificationTokenDto, ForgotPasswordDto, ResetPasswordDto, ChangePasswordDto
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

    @jwt_required()
    @blp.arguments(ChangePasswordDto)
    def put(self, params):
        current_user_id = get_jwt_identity()
        current_user_role = get_jwt()['role']
        public_id = params['public_id']
        password = params['password']
        new_password = params['new_password']
        return auth_service.change_password(
            current_user_id,
            current_user_role,
            public_id,
            password,
            new_password
        )
