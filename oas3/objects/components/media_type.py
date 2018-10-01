"""
oas3.objects.components.media_type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from marshmallow import fields
from oas3.util import RefOrSchema
from oas3.base import BaseObject, BaseSchema
from .schema import Schema


class MediaType(BaseObject):
    """
    Each Media Type Object provides schema and examples for the media
    type identified by its key.

    .. note:
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#mediaTypeObject
    """

    class Schema(BaseSchema):
        schema = RefOrSchema(Schema.Schema)
        example = fields.Raw()
        examples = fields.Dict(keys=fields.Str, values=fields.Dict)
        encoding = fields.Dict(keys=fields.Str, values=fields.Dict)

        def represents(self):
            return MediaType

    def __init__(self, schema=None, example=None, examples=None, encoding=None):
        self.schema = schema
        self.example = example
        self.examples = examples
        self.encoding = encoding
