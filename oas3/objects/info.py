"""
oas3.objects.info
~~~~~~~~~~~~~~~~~
"""

from marshmallow import fields
from oas3.base import BaseObject, BaseSchema


class Contact(BaseObject):
    """
    Contact information for the exposed API.

    .. note:
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#contactObject
    """

    class Schema(BaseSchema):
        name = fields.Str(required=True)
        url = fields.Url(required=True)
        email = fields.Email()

        def represents(self):
            return Contact

    def __init__(self, name, url, email=None):
        self.name = name
        self.url = url
        self.email = email


class License(BaseObject):
    """
    License information for the exposed API.

    .. note:
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#licenseObject
    """
    class Schema(BaseSchema):
        name = fields.Str(required=True)
        url = fields.Url()

        def represents(self):
            return License

    def __init__(self, name, url=None):
        self.name = name
        self.url = url


class Info(BaseObject):
    """
    Info object provides metadata about the API.

    .. note:
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.1.md#infoObject
    """

    class Schema(BaseSchema):
        version = fields.Str(required=True)
        title = fields.Str(required=True)
        description = fields.Str(required=False)
        terms_of_service = fields.Str(load_from='termsOfService', dump_to='termsOfService')
        contact = fields.Nested(Contact.Schema)
        license = fields.Nested(License.Schema)

        def represents(self):
            return Info

    def __init__(self, title, version, description=None, terms_of_service=None, contact=None, license=None):
        self.title = title
        self.version = version
        self.description = description
        self.terms_of_service = terms_of_service
        self.contact = contact
        self.license = license
