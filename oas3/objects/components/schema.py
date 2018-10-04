"""
oas3.objects.components.schema
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from marshmallow import fields
from oas3.base import BaseObject, BaseSchema


class Schema(BaseObject):
    """
    The Schema Object allows the definition of input and output data types.
    These types can be objects, but also primitives and arrays. This object is
    an extended subset of the JSON Schema Specification Wright Draft 00.

    .. note:
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#schemaObject
    """

    class Schema(BaseSchema):
        #title =
        #multiple_of =
        #maximum =
        #exclusive_maximum =
        #minimum =
        #exclusive_minimum =
        #max_length =
        #min_length =
        #pattern =
        #max_items =
        #min_items =
        #unique_items =
        #max_properties =
        #min_properties =
        required = fields.List(fields.Str)
        #enum =
        schema_type = fields.Str(load_from='type', dump_to='type')
        all_of = fields.List(fields.Raw, load_from='allOf', dump_to='allOf')
        #one_of =
        #any_of =
        #not_of =
        items = fields.Dict()
        properties = fields.Dict()
        #additional_properties =
        #description =
        #schema_format =
        #default =
        #nullable =
        #read_only =
        #write_only =
        #xml =
        #external_docs =
        example = fields.Dict()
        #deprecated =

        def represents(self):
            return Schema

    def __init__(self, properties=None, required=None, schema_type=None, all_of=None, example=None):
        self.properties = properties
        self.required = required
        self.schema_type = schema_type
        self.all_of = all_of
        self.example = example
