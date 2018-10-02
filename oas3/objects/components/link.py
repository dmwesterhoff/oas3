"""
oas3.objects.components.link
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from marshmallow import fields
from oas3.base import BaseObject, BaseSchema
from oas3.objects.server import Server


class Link(BaseObject):
    """
    The Link object represents a possible design-time link for a response.
    The presence of a link does not guarantee the caller's ability to
    successfully invoke it, rather it provides a known relationship and
    traversal mechanism between responses and other operations.

    .. note:
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#linkObject
    """

    class Schema(BaseSchema):
        operation_ref = fields.Str(load_from='operationRef',
                                   dump_to='operationRef')
        operation_id = fields.Str(load_from='operationId',
                                  dump_to='operationId')
        parameters = fields.Dict(keys=fields.Str, values=fields.Dict)
        request_body = fields.Dict(load_from='requestBody',
                                   dump_to='requestBody')
        description = fields.Str()
        server = fields.Nested(Server.Schema)

        def represents(self):
            return Link

    def __init__(self, operation_ref=None, operation_id=None, parameters=None, request_body=None, description=None, server=None):
        self.operation_ref = operation_ref
        self.operation_id = operation_id
        self.parameters = parameters
        self.request_body = request_body
        self.description = description
        self.server = server
