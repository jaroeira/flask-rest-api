from uuid import uuid4
from app.db import db
from app.models import UserModel
from typing import Dict
from flask import current_app
from flask_smorest import abort
from sqlalchemy import or_
from datetime import datetime
from app.utils import generate_random_hash
from tasks import send_verification_email
from app.utils import save_db_item, delete_db_item


def create_user(user_data: Dict[str, str]):
    if UserModel.query.filter(UserModel.username == user_data["username"]
                              ).first():
        abort(409, message="A user with that email or username already exists.")

    # The very first user to be registered will be admin by default
    if UserModel.query.count() == 0:
        user_data['role'] = 'admin'
        user_data['email_verified'] = True

    verification_token = generate_random_hash()
    email_verified = user_data.get("email_verified", False)

    new_user = UserModel(
        public_id=str(uuid4()),
        email=user_data["email"].lower(),
        username=user_data["username"].lower(),
        password=user_data["password"],
        role=user_data.get("role", "user").lower(),
        email_verified=email_verified,
        verification_token=verification_token if not email_verified else None
    )

    save_db_item(new_user, db)

    if not new_user.email_verified:
        current_app.tasks_queue.enqueue(
            send_verification_email, new_user.email, new_user.username, verification_token)

    return {"message": "User created successfully!", "public_id": new_user.public_id}, 201


def get_all_users():
    return UserModel.query.all()


def get_user_by_id(public_id: str):
    user = UserModel.query.filter_by(public_id=public_id).first()
    if not user:
        abort(404)
    return user


def update_user(user_data):
    user: UserModel = UserModel.query.filter_by(
        public_id=user_data['public_id']).first()
    if not user:
        abort(404)

    if user_data["email"] != user.email and _check_if_email_exists(user_data["email"]):
        abort(409, message="A user with that email already exists.")

    if user_data["username"] != user.username and _check_if_username_exists(user_data["username"]):
        abort(409, message="A user with that username already exists.")

    user.email = str(user_data["email"]).lower()
    user.username = str(user_data["username"]).lower()
    user.role = str(user_data["role"]).lower()
    user.email_verified = user_data["email_verified"]
    user.updated_at = datetime.now()

    save_db_item(user, db)
    return {"message": "User updated successfully!"}, 200


def remove_user_by_id(public_id: str):
    user = UserModel.query.filter_by(public_id=public_id).first()
    if not user:
        abort(404)
    delete_db_item(user, db)
    return {"message": "User deleted successfully!"}, 200


def _check_if_email_exists(email: str) -> bool:
    return UserModel.query.filter_by(email=email).first() != None


def _check_if_username_exists(username: str) -> bool:
    return UserModel.query.filter_by(username=username).first() != None


