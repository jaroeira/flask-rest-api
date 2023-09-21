from typing import Dict
from app.models import UserModel
from flask_smorest import abort
from flask_jwt_extended import create_access_token, set_access_cookies
from flask import jsonify
from app.db import db
from sqlalchemy.exc import SQLAlchemyError


def signin_user(user_data: Dict[str, str]):
    username = user_data["username"]
    password = user_data["password"]

    user: UserModel = UserModel.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        abort(401, message="Username or password incorrect")

    response = jsonify({
        "public_id": user.public_id,
        "role": user.role
    })

    additional_claims = {"role": user.role}

    access_token = create_access_token(
        identity=user.public_id, additional_claims=additional_claims)
    set_access_cookies(response, access_token)

    return response, 200


def verify_user_email(verification_token: str):
    user: UserModel = UserModel.query.filter_by(
        verification_token=verification_token).first()
    if not user:
        abort(403, message="verification failed. invalid token")

    user.email_verified = True
    user.verification_token = None

    _save_user_changes(user)

    return {"message": "email address was successfully verified"}, 200


def _save_user_changes(user: UserModel):
    try:
        db.session.add(user)
        db.session.commit()
    except SQLAlchemyError as e:
        print(e)
        abort(500, message="An error occurred.")
