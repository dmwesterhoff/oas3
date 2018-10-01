"""
oas3.objects.components.callback
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from marshmallow import fields
from oas3.base import BaseObject, BaseSchema


class Callback(BaseObject):
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
            return Callback

    def __init__(self, schemas=None):
        pass
