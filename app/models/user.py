from app.db import db
import bcrypt
from sqlalchemy.sql import func

class UserModel(db.Model):
     """ User Model for storing user data"""
     __tablename__ = "users"

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
     updated_at = db.Column(db.DateTime, nullable=False, default=func.now())
     created_at = db.Column(db.DateTime, nullable=False, default=func.now())


     @property
     def password(self):
        raise AttributeError('password: write-only field')
     
     @password.setter
     def password(self, plain_password: str):
          salt = bcrypt.gensalt()
          hashed_password_bytes = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
          self.password_hash = hashed_password_bytes.decode('utf-8')

     def verify_password(self, plain_password: str) -> bool:
          return bcrypt.checkpw(plain_password.encode('utf-8'), self.password_hash.encode('utf-8'))
     
     def __repr__(self):
        return f"<User '{self.username}'>"
