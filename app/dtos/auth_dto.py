from marshmallow import Schema, fields


class EmailVerificationTokenDto(Schema):
    token = fields.Str(required=True)
