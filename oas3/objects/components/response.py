"""
oas3.objects.components.response
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from marshmallow import fields
from oas3.base import BaseObject, BaseSchema
from oas3.util import RefOrSchema
from oas3.objects.components.media_type import MediaType


class Response(BaseObject):
    """
    Describes a single response from an API Operation, including design-time,
    static links to operations based on the response.

    .. note:
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#responseObject
    """

    class Schema(BaseSchema):
        description = fields.Str(required=True)
        headers = fields.Dict()
        content = fields.Dict(keys=fields.Str, values=RefOrSchema(MediaType.Schema))
        links = fields.Dict()

        def represents(self):
            return Response

    def __init__(self, description, headers=None, content=None, links=None):
        self.description = description
        self.headers = headers
        self.content = content
        self.links = links
