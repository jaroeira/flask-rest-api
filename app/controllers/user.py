from flask.views import MethodView
from flask_smorest import Blueprint
from app.dtos import CreateUserDto
from app.services.user_service import create_user

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

    def get(self):
        """Get a list of all users - Admin only"""
        return {"message": "get a list with all users - endpoint - TODO"}, 200

    @blp.arguments(CreateUserDto)
    def post(self, user_data):
        """Create user - Admin only"""
        return create_user(user_data)
       
    
    def put(self):
        """Update user - Admin only"""
        return {"message": "update user endpoint - TODO"}, 200
    

@blp.route("/<int:user_id>")
class UserById(MethodView):

    def get(self, user_id):
        return {"message": f"get user by id endpoint - TODO - id passed: {user_id}"}, 200
    
    def delete(self, user_id):
        return {"message": f"delete user by id endpoint - TODO - id passed: {user_id}"}, 200