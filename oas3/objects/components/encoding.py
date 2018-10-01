"""
oas3.objects.components.encoding
~~~~~~~~~~~~~
"""

from marshmallow import fields
from oas3.base import BaseObject, BaseSchema


class Encoding(BaseObject):
    """
    A single encoding definition applied to a single schema property.

    .. note:
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#encodingObject
    """

    class Schema(BaseSchema):
        content_type = fields.Str(load_from='contentType')
        headers = fields.Dict(keys=fields.Str, values=fields.Dict)
        style = fields.Str()
        explode = fields.Bool()
        allow_reserved = fields.Bool(load_from='allowReserved')

        def represents(self):
            return Encoding

    def __init__(self, content_type=None, headers=None, style=None, explode=None, allow_reserved=None):
        self.content_type = content_type
        self.headers = headers
        self.style = style
        self.explode = explode
        self.allow_reserved = allow_reserved
