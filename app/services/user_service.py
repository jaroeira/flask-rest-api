from uuid import uuid4
from app.db import db
from app.models import UserModel
from typing import Dict
from flask_smorest import abort
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_

def create_user(user_data: Dict[str, str]):
    if UserModel.query.filter(
        or_(UserModel.username ==
                user_data["username"], UserModel.email == user_data["email"])
        ).first():
        abort(409, message="A user with that email or username already exists.")

    new_user = UserModel(
        public_id = str(uuid4()),
        email = user_data["email"],
        username = user_data["username"],
        password = user_data["password"],
        role = user_data["role"]
    )

    _save_changes(new_user)

    return {"message": "User created successfully!"}, 201

def get_all_users():
    return UserModel.query.all()

def get_user_by_id(public_id: str):
    user = UserModel.query.filter_by(public_id=public_id).first()
    if not user:
        abort(404)
    return user

def remove_user_by_id(public_id: str):
    user = UserModel.query.filter_by(public_id=public_id).first()
    if not user:
        abort(404)
    _delete_user(user)
    return {"message": "User deleted successfully!"}, 200
    

def _save_changes(user: UserModel):
    try:
        db.session.add(user)
        db.session.commit()   
    except SQLAlchemyError as e:
        print(e)
        abort(500, message="An error occurred.")  

def _delete_user(user: UserModel):
    try:
        db.session.delete(user)
        db.session.commit()   
    except SQLAlchemyError as e:
        print(e)
        abort(500, message="An error occurred.")  
