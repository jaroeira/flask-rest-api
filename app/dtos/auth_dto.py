from marshmallow import Schema, fields, ValidationError, validates
from app.utils import is_valid_email


class EmailVerificationTokenDto(Schema):
    token = fields.Str(required=True)


class ForgotPasswordDto(Schema):
    email = fields.Str(required=True)

    @validates("email")
    def validate_email(self, value):
        if not is_valid_email(value):
            raise ValidationError("Invalid email address")


class ResetPasswordDto(Schema):
    token = fields.Str(required=True)
    new_password = fields.Str(required=True)
