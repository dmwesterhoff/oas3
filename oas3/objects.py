"""
flask.objects
~~~~~~~~~~~~~

Defines the objects that are enumarated in the OAS3 specification

.. note::
    https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#schema
"""

import yaml
from pprint import pformat
from inspect import cleandoc
from marshmallow import fields, Schema, pprint, post_load, post_dump


class BaseObject(object):
    """
    Implements a base class that all OAS 3 objects inherit from.
    """
    data = {}

    def __str__(self):
        return pformat(self.data)

    def __init__(self, obj, schema):
        docstring = cleandoc(obj.__doc__)
        dictionary = yaml.load(docstring)
        result = schema().load(dictionary)
        for key, value in result.errors.items():
            print("`{}` {}".format(key, value[0]))
            raise ValueError(value)
        self.data = result.data


class Contact(BaseObject):
    """
    Contact information for the exposed API.

    .. note:
    https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#infoObject
    """

    class Meta(Schema):
        name = fields.Str(required=True)
        url = fields.Url(required=True)
        email = fields.Email()

    def __init__(self, obj):
        BaseObject.__init__(self, obj, self.Meta)
        self.name = self.data['name']


class License(BaseObject):
    """
    License information for the exposed API.

    .. note:
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#infoObject
    """
    class Meta(Schema):
        name = fields.Str(required=True)
        url = fields.Url(required=True)

    def __init__(self, obj):
        BaseObject.__init__(self, obj, self.Meta)
        self.name = self.data['name']


class Info(BaseObject):
    """
    Info object provides metadata about the API.

    .. note:
    https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#infoObject
    """

    class Meta(Schema):
        version = fields.Str(required=True)
        title = fields.Str(required=True)
        description = fields.Str(required=False)
        terms_of_service = fields.Str(load_from='termsOfService')
        contact = fields.Nested(Contact.Meta)
        license = fields.Nested(License.Meta)

        @post_dump
        def skip_none_values(self, data):
            """Skips any values that are None because they were not provided."""
            return {
                key: value for key, value in data.items()
                if value is not None
            }

        @post_load
        def make_spec(self, data):
            return Info(**data)

    def __init__(self, title, version, description=None, terms_of_service=None, contact=None, license=None):
        self.title = title
        self.version = version
        self.description = description
        self.terms_of_service = terms_of_service
        self.contact = contact
        self.license = license

    @classmethod
    def load_from_class(cls, obj_cls):
        """Initializes via a class YAML docstring."""
        docstring = cleandoc(obj_cls.__doc__)
        dictionary = yaml.load(docstring)
        result, errors = cls.Meta().load(dictionary)
        if errors:
            raise ValueError("Validation error encountered in [{}] ".format(obj_cls.__name__) \
                             + str(errors))
        return result


class Spec(object):
    """

    .. note:
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#oasObject
    """
    class Meta(Schema):
        openapi = fields.Str(required=True)
        info = fields.Nested(Info.Meta, required=True)

        @post_load
        def make_spec(self, data):
            return Spec(**data)

    def __init__(self, openapi, info):
        self.openapi = openapi
        self.info = info


"""
https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#contactObject
https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#licenseObject
https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#serverObject
https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#serverVariableObject
https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#componentsObject
https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#pathsObject
https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#pathItemObject
https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#operationObject
https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#externalDocumentationObject
https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#parameterObject
https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#requestBodyObject
https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#mediaTypeObject
https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#encodingObject
https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#responsesObject
https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#responseObject
https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#callbackObject
https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#exampleObject
https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#linkObject
https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#headerObject
https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#tagObject
https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#referenceObject
https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#schemaObject
https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#discriminatorObject
https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#xmlObject
https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#securitySchemeObject
https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#oauthFlowsObject
https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#oauthFlowObject
https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#securityRequirementObject
"""
