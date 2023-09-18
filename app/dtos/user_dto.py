from marshmallow import Schema, ValidationError, fields, validates
from app.utils import is_valid_email


class UserDto(Schema):
    email = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

    @validates("email")
    def validate_email(self, value):
        if not is_valid_email(value):
            raise ValidationError("Invalid email address")


class CreateUserDto(UserDto):
    role = fields.Str(required=True)

class FullUserToReturnDto(UserDto):
     role = fields.Str()
     public_id = fields.Str()
     last_password_reset = fields.DateTime()
     password_changed = fields.DateTime()
     email_verified = fields.Bool()
     updated_at = fields.DateTime()
     created_at = fields.DateTime()



    
