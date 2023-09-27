from marshmallow import Schema, fields, ValidationError, pre_load, validates
from flask_smorest.fields import Upload


class TagDto(Schema):
    name = fields.Str()


class ArticleToReturnDto(Schema):

    title = fields.Str()
    slug = fields.Str()
    description = fields.Str()
    content = fields.Str()
    tags = fields.List(fields.Nested(TagDto()), dump_only=True)
    likes = fields.Int(dump_only=True)
    created_at = fields.DateTime()


class PaginatedArticlesDto(Schema):
    page = fields.Int()
    page_size = fields.Int()
    total_pages = fields.Int()
    total_items = fields.Int()
    has_next = fields.Bool()
    has_prev = fields.Bool()
    data = fields.List(fields.Nested(ArticleToReturnDto()))


class ArticleToInsertDto(Schema):
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    content = fields.Str(required=True)
    tags = fields.List(fields.Str, required=True)

    @validates("tags")
    def validate_tags(self, value):
        if len(value) == 0:
            raise ValidationError("A least one tag is required.")

    @pre_load
    def normalize_tags(self, data, **kwargs):
        return _normalize_tags(data)


class ArticleToUpdateDto(ArticleToInsertDto):
    slug = fields.Str(required=True)


def _normalize_tags(data):
    if "tags" in data and isinstance(data["tags"], list):
        data["tags"] = [tag.lower() for tag in data["tags"]]
    return data


class ArticleSearchTerm(Schema):
    term = fields.Str(required=True)


class ArticleUploadImageDto(Schema):
    image = Upload(required=True)
