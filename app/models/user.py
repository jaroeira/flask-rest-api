from app import db

class User(db.Model):
     """ User Model for storing user data"""
     __tablename___ = "user"

     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
     email = db.Column(db.String(255), unique=True, nullable=False)
     username = db.Column(db.String(50), unique=True)
     password_hash = db.Column(db.String(100))
     role = db.Column(db.String(10), nullable=False, default="user")
     public_id = db.Column(db.String(100), unique=True)
     last_password_reset = db.Column(db.DateTime, nullable=True)
     password_changed = db.Column(db.DateTime, nullable=True)
     reset_token = db.Column(db.String(255))
     reset_token_expiration = db.Column(db.DateTime, nullable=True)
     verification_token = db.Column(db.String(255))
     email_verified = db.Column(db.Boolean, nullable=False, default=False)
     updated_at = db.Column(db.DateTime, nullable=False)
     created_at = db.Column(db.DateTime, nullable=False)