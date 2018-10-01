"""
oas3.objects.components.request_body
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from marshmallow import fields
from oas3.base import BaseObject, BaseSchema


class RequestBody(BaseObject):
    """
    Describes a single request body.

    .. note:
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#requestBodyObject
    """

    class Schema(BaseSchema):
        content = fields.Dict(required=True, keys=fields.Str, values=fields.Dict)
        description = fields.Str()
        required = fields.Bool()

        def represents(self):
            return RequestBody

    def __init__(self, content, description=None, required=None):
        self.content = content
        self.description = description
        self.required = required
