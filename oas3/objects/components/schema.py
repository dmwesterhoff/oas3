"""
oas3.objects.components.schema
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from marshmallow import fields
from oas3.base import BaseObject, BaseSchema


class Schema(BaseObject):
    """
    Holds a set of reusable objects for different aspects of the OAS.
    All objects defined within the components object will have no effect on the API
    unless they are explicitly referenced from properties outside the components object.

    .. note:
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#componentsObject
    """

    class Schema(BaseSchema):
        pass

        def represents(self):
            return Schema

    def __init__(self, schemas=None):
        self.schemas = schemas
