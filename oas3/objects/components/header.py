"""
oas3.objects.components.header
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from marshmallow import fields
from oas3.base import BaseObject, BaseSchema


class Header(BaseObject):
    """

    .. note:
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#headerObject
    """

    class Schema(BaseSchema):
        pass

        def represents(self):
            return Header

    def __init__(self):
        pass
