"""
oas3.objects.external_docs
~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from marshmallow import fields
from oas3.base import BaseObject, BaseSchema


class ExternalDocs(BaseObject):
    """
    Allows referencing an external resource for extended documentation.

    .. note:
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#externalDocumentationObject
    """

    class Schema(BaseSchema):
        url = fields.Url(required=True)
        description = fields.Str()

        def represents(self):
            return ExternalDocs

    def __init__(self, url, description=None):
        self.url = url
        self.description = description
