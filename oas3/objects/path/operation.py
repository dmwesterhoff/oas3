"""
oas3.objects.path.operation
~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from marshmallow import fields
from oas3.base import BaseObject, BaseSchema
from oas3.objects.external_docs import ExternalDocs
from oas3.objects.server import Server
from oas3.objects.components.response import Response
from oas3.objects.components.request_body import RequestBody
from oas3.objects.components.parameter import Parameter


class Operation(BaseObject):
    """
    Describes a single API operation on a path.

    .. note:
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#operationObject
    """

    class Schema(BaseSchema):
        responses = fields.Dict(required=True, keys=fields.Str, values=fields.Nested(Response.Schema))
        tags = fields.List(fields.Str)
        summary = fields.Str()
        description = fields.Str()
        external_docs = fields.Nested(ExternalDocs.Schema,
                                      load_from='externalDocs',
                                      dump_to='externalDocs')
        operation_id = fields.Str()
        parameters = fields.List(fields.Nested(Parameter.Schema))
        request_body = fields.Nested(RequestBody.Schema,
                                     load_from='requestBody',
                                     dump_to='requestBody')
        # FIXME: Use Callback.Schema
        callbacks = fields.Dict(keys=fields.Str,
                                values=fields.Dict(keys=fields.Str,
                                                   values=fields.Dict()))
        deprecated = fields.Bool()
        security = fields.List(fields.Dict(keys=fields.Str,
                                           values=fields.List(fields.Str)))
        servers = fields.List(fields.Nested(Server.Schema))

        def represents(self):
            return Operation

    def __init__(self, responses, tags=None, summary=None, description=None, external_docs=None, operation_id=None, parameters=None, request_body=None, callbacks=None, deprecated=None, security=None, servers=None):
        self.responses = responses
        self.tags = tags
        self.summary = summary
        self.description = description
        self.external_docs = external_docs
        self.operation_id = operation_id
        self.parameters = parameters
        self.request_body = request_body
        self.callbacks = callbacks
        self.deprecated = deprecated
        self.security = security
        self.servers = servers
