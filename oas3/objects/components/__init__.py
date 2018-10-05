"""
oas3.objects.components
~~~~~~~~~~~~~~~~~~~~~~~
"""

from marshmallow import fields
from oas3.base import BaseObject, BaseSchema
from .schema import Schema
from .response import Response
from .example import Example
from .parameter import Parameter
from .request_body import RequestBody
from .header import Header
from .security_scheme import SecurityScheme
from .link import Link
from .callback import Callback


class Components(BaseObject):
    """
    Holds a set of reusable objects for different aspects of the OAS.
    All objects defined within the components object will have no effect on the API
    unless they are explicitly referenced from properties outside the components object.

    .. note:
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#componentsObject
    """

    class Schema(BaseSchema):
        schemas = fields.Dict(keys=fields.Str,
                              values=fields.Nested(Schema.Schema))
        responses = fields.Dict()
        parameters = fields.Dict()
        examples = fields.Dict()
        response_bodies = fields.Dict(load_from='responseBodies',
                                      dump_to='responseBodies')
        headers = fields.Dict()
        security_schemes = fields.Dict(load_from='securitySchemes',
                                       dump_to='securitySchemes')
        links = fields.Dict()
        callbacks = fields.Dict()

        def represents(self):
            return Components

    def __init__(self,
                 schemas=None,
                 responses=None,
                 parameters=None,
                 examples=None,
                 response_bodies=None,
                 headers=None,
                 security_schemes=None,
                 links=None,
                 callbacks=None):
        self.schemas = schemas
        self.responses = responses
        self.examples = examples
        self.response_bodies = response_bodies
        self.headers = headers
        self.security_schemes = security_schemes
        self.links = links
        self.callbacks = callbacks
