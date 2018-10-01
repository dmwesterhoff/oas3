"""
oas3
~~~~
OAS3 is a package that makes compiling, parsing, validating and converting
Open API v3 specifications simple and pythonic. The library aims to be useful
as a core library for creating higher level OAS3 packages.
"""

# Versioneer
# ----------
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


import pathlib
import json
import yaml
import requests
from marshmallow import fields, post_load, post_dump
from .base import BaseObject, BaseSchema
from .objects.info import Info
from .objects.server import Server
from .objects.components import Components
from .objects.tag import Tag
from .objects.external_docs import ExternalDocs
from .objects.path import Path
from .errors import LoadingError, DumpingError, ValidationError


class Spec(BaseObject):
    """
    High level interface around compiling, validation parsing and loading an OAS3 spec.

    The process typically involves loading data from a source, then the following occurs
        - Data is validated
        - Input is serialized to python objects
        - Resolving references
        - OAS3 is validated
        - Reference resolved to other objects in the spec

    Example:
        >>> from oas3 import Spec
    """

    class Schema(BaseSchema):
        openapi = fields.Str(required=True)
        info = fields.Nested(Info.Schema, required=True)
        paths = fields.Dict(required=True, keys=fields.Str, values=Path.Schema)
        servers = fields.List(fields.Nested(Server.Schema))
        components = fields.Nested(Components.Schema)
        security = fields.List(fields.Dict(keys=fields.Str,
                                           values=fields.List(fields.Str)))
        tags = fields.List(fields.Nested(Tag.Schema))
        external_docs = fields.Nested(ExternalDocs.Schema, load_from='externalDocs')

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





# from .oas3 import OAS3
# from . import objects
# from . import primitives
