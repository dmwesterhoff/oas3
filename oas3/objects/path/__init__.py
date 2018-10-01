"""
oas3.objects.path
~~~~~~~~~~~~~~~~~
"""

from marshmallow import fields
from oas3.base import BaseObject, BaseSchema
from oas3.objects.server import Server
from .operation import Operation
from oas3.objects.components.parameter import Parameter



class Path(BaseObject):
    """
    Adds metadata to a single tag that is used by the Operation Object.
    It is not mandatory to have a Tag Object per tag defined in the
    Operation Object instances.

    .. note:
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#pathItemObject
    """

    class Schema(BaseSchema):
        ref = fields.Str()
        summary = fields.Str()
        description = fields.Str()
        get = fields.Nested(Operation.Schema)
        post = fields.Nested(Operation.Schema)
        put = fields.Nested(Operation.Schema)
        patch = fields.Nested(Operation.Schema)
        delete = fields.Nested(Operation.Schema)
        options = fields.Nested(Operation.Schema)
        trace = fields.Nested(Operation.Schema)
        head = fields.Nested(Operation.Schema)
        servers = fields.List(fields.Nested(Server.Schema))
        parameters = fields.List(fields.Nested(Parameter.Schema))

        def represents(self):
            return Path

    def __init__(self, ref=None, summary=None, description=None, get=None, post=None, put=None, patch=None, delete=None, options=None, trace=None, head=None, servers=None, parameters=None):
        self.ref = ref
        self.summary = summary
        self.description = description
        self.get = get
        self.post = post
        self.put = put
        self.delete = delete
        self.options = options
        self.trace = trace
        self.head = head
        self.servers = servers
        self.parameters = parameters
