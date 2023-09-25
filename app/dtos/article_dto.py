from marshmallow import Schema, fields, ValidationError, pre_load, validates


class TagDto(Schema):
    name = fields.Str()


class ArticleToReturnDto(Schema):
   
    title = fields.Str()
    slug = fields.Str()
    description = fields.Str()
    content = fields.Str()
    tags = fields.List(fields.Nested(TagDto()), dump_only=True)


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