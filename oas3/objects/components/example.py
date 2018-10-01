"""
oas3.objects.components.example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from marshmallow import fields
from oas3.base import BaseObject, BaseSchema


class Example(BaseObject):
    """

    .. note:
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#exampleObject
    """

    class Schema(BaseSchema):
        summary = fields.Str()
        description = fields.Str()
        value = fields.Raw()

        def represents(self):
            return Example

    def __init__(self, summary=None, description=None, value=None):
        self.summary = summary
        self.description = description
        self.value = value
