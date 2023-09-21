from marshmallow import Schema, fields


class EmailVerificationTokenDto(Schema):
    token = fields.String(
        required=True,
        description="Verification Token sent to the users email"
    )
