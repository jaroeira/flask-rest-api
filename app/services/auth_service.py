from typing import Dict
from app.models import UserModel
from flask_smorest import abort
from flask_jwt_extended import create_access_token


def signin_user(user_data: Dict[str, str]):
    username = user_data["username"]
    password = user_data["password"]

    user: UserModel =  UserModel.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        abort(401, "Username or password incorrect")

    access_token = create_access_token(identity=user.public_id, fresh=True)

    return {
        "access_token": access_token,
        "public_id": user.public_id,
        "role": user.role
        }, 200
