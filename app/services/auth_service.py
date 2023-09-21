from typing import Dict
from app.models import UserModel
from flask_smorest import abort
from flask_jwt_extended import create_access_token, set_access_cookies
from flask import jsonify
from app.db import db
from sqlalchemy.exc import SQLAlchemyError
from app.utils import generate_random_hash
from datetime import datetime, timedelta
from tasks import send_password_reset_email


def signin_user(user_data: Dict[str, str]):
    username = user_data["username"]
    password = user_data["password"]

    user: UserModel = UserModel.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        abort(401, message="Username or password incorrect")

    if not user.email_verified:
        abort(401, message="Sorry. User\'s email must be verified before first sign in")

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


def forgot_password(email: str):
    user: UserModel = UserModel.query.filter_by(email=email).first()

    if not user:
        return {}, 200

    reset_token = generate_random_hash()
    reset_token_expiration = datetime.now() + timedelta(days=1)

    user.reset_token = reset_token
    user.reset_token_expiration = reset_token_expiration

    _save_user_changes(user)

    send_password_reset_email(user.email, user.reset_token)

    return {}, 200


def reset_password(reset_token, new_password):
    user: UserModel = UserModel.query.filter_by(
        reset_token=reset_token).first()

    current_datetime = datetime.now()

    if not user or user.reset_token_expiration < current_datetime:
        abort(403, message="Invalid reset password token")

    user.password = new_password
    user.reset_token = None
    user.reset_token_expiration = None
    user.last_password_reset = datetime.now()
    user.updated_at = datetime.now()

    _save_user_changes(user)

    return {"message": "The password has been successfully reset"}, 200


def _save_user_changes(user: UserModel):
    try:
        db.session.add(user)
        db.session.commit()
    except SQLAlchemyError as e:
        print(e)
        abort(500, message="An error occurred.")
