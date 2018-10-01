"""
oas3.objects.tag
~~~~~~~~~~~~~~~~
"""

from marshmallow import fields
from oas3.base import BaseObject, BaseSchema
from .external_docs import ExternalDocs


class Tag(BaseObject):
    """
    Adds metadata to a single tag that is used by the Operation Object.
    It is not mandatory to have a Tag Object per tag defined in the
    Operation Object instances.

    .. note:
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#tagObject
    """

    class Schema(BaseSchema):
        name = fields.Str(required=True)
        description = fields.Str()
        external_docs = fields.Nested(ExternalDocs.Schema)

        def represents(self):
            return Tag

    def __init__(self, name, description=None, external_docs=None):
        self.name = name
        self.description = description
        self.external_docs = external_docs
