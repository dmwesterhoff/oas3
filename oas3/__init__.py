"""
oas3
~~~~
OAS3 is a package that makes compiling, parsing, validating and converting
Open API v3 specifications simple and pythonic. The library aims to be useful
as a core library for creating higher level OAS3 packages.
"""

# Versioneer
# ----------
from marshmallow import fields
from .base import BaseObject, BaseSchema
from .objects.info import Info
from .objects.server import Server
from .objects.tag import Tag
from .objects.external_docs import ExternalDocs
from .objects.components import Components, Schema
from .objects.path import Path, Operation
from .errors import LoadingError, DumpingError, ValidationError  # NOQA
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


class Spec(BaseObject):
    """
    High level interface around compiling, validating, parsing and loading an OAS3 spec.
    """

    class Schema(BaseSchema):
        openapi = fields.Str(required=True)  # FIXME: should use default value
        info = fields.Nested(Info.Schema, required=True)
        paths = fields.Dict(required=True, keys=fields.Str, values=Path.Schema)
        servers = fields.List(fields.Nested(Server.Schema))
        components = fields.Nested(Components.Schema)
        security = fields.List(fields.Dict(keys=fields.Str,
                                           values=fields.List(fields.Str)))
        tags = fields.List(fields.Nested(Tag.Schema))
        external_docs = fields.Nested(ExternalDocs.Schema,
                                      load_from='externalDocs',
                                      dump_to='externalDocs')

        def represents(self):
            return Spec

    def __init__(self,
                 openapi=None,
                 info=None,
                 paths=None,
                 servers=None,
                 components=None,
                 security=None,
                 tags=None,
                 external_docs=None):
        self.openapi = openapi
        self.info = info
        self.paths = paths
        self.servers = servers
        self.components = components
        self.security = security
        self.tags = tags
        self.external_docs = external_docs

    def to_dict(self):
        """
        Converts all internal data type to raw dictionaries with
        built-in values.

        :returns dict: Dictionary representing the spec
        :raises ValidationError: Spec was incomplete or had errors
        """
        data, errors = self.Schema().dump(self)
        for key, value in self.paths.items():
            if isinstance(value, Path):
                self.paths[key] = value.to_dict()
        for key, value in self.components.schemas.items():
            if isinstance(value, Schema):
                self.components.schemas[key] = value.to_dict()
        if errors:
            raise ValidationError(errors)
        errors = self.Schema().validate(data)
        if errors:
            raise ValidationError(errors)
        return data
