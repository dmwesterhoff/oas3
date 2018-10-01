"""
oas3.objects.server
~~~~~~~~~~~~~~~~~~~
"""

from marshmallow import fields
from oas3.base import BaseObject, BaseSchema


class ServerVariable(BaseObject):
    """
    An object representing a Server Variable for server URL template substitution.

    .. note:
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#serverVariableObject
    """

    class Schema(BaseSchema):
        default = fields.Str(required=True)
        enum = fields.List(fields.Str)
        description = fields.Str()

        def represents(self):
            return ServerVariable

    def __init__(self, default, enum=None, description=None):
        self.default = default
        self.enum = enum
        self.description = description


class Server(BaseObject):
    """
    An object representing a Server.

    .. note:
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#serverObject
    """

    class Schema(BaseSchema):
        url = fields.Str(required=True)
        description = fields.Url()
        variables = fields.Dict(keys=fields.Str,
                                values=fields.Nested(ServerVariable.Schema))

        def represents(self):
            return Server

    def __init__(self, url, description=None, variables=None):
        self.url = url
        self.description = description
        self.variables = variables
