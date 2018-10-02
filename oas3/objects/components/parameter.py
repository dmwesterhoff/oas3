"""
oas3.objects.components.parameter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from marshmallow import fields
from oas3.base import BaseObject, BaseSchema


class Parameter(BaseObject):
    """
    Holds a set of reusable objects for different aspects of the OAS.
    All objects defined within the components object will have no effect on the API
    unless they are explicitly referenced from properties outside the components object.

    .. note:
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#componentsObject
    """

    class Schema(BaseSchema):
        name = fields.Str(required=True)
        location = fields.Str(required=True,
                              load_from='in',
                              dump_to='in')
        description = fields.Str()
        required = fields.Bool()
        deprecated = fields.Bool()
        allow_empty_value = fields.Bool(load_from='allowEmptyValue',
                                        dump_to='allowEmptyValue')
        style = fields.Str()
        explode = fields.Bool()
        allow_reserved = fields.Bool(load_from='allowReserved',
                                     dump_to='allowReserved')
        schema = fields.Dict()
        example = fields.Raw()
        examples = fields.Dict(keys=fields.Str, values=fields.Dict)

        def represents(self):
            return Parameter

    def __init__(self, name, location, description=None, required=None, deprecated=None, allow_empty_value=None, style=None, explode=None, allow_reserved=None, schema=None, example=None, examples=None):
        self.name = name
        self.location = location
        self.description = description
        self.required = required
        self.deprecated = deprecated
        self.allow_empty_value = allow_empty_value
        self.style = style
        self.explode = explode
        self.allow_reserved = allow_reserved
        self.schema = schema
        self.example = example
        self.examples = examples
