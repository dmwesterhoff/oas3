"""
oas3.objects.components.security_scheme
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from marshmallow import fields
from oas3.base import BaseObject, BaseSchema


class OAuthFlow(BaseObject):
    """
    Configuration details for a supported OAuth Flow

    .. note:
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#oauthFlowObject
    """

    class Schema(BaseSchema):
        authorization_url = fields.Url(load_from='authorizationUrl')
        token_url = fields.Url(load_from='tokenUrl')
        refresh_url = fields.Url(load_from='refreshUrl')
        scopes = fields.Dict(keys=fields.Str, values=fields.Str)

        def represents(self):
            return OAuthFlow

    def __init__(self, authorization_url=None, token_url=None, refresh_url=None, scopes=None):
        self.authorization_url = authorization_url
        self.token_url = token_url
        self.refresh_url = refresh_url
        self.scopes = scopes


class OAuthFlows(BaseObject):
    """
    Allows configuration of the supported OAuth Flows.

    .. note:
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#oauthFlowsObject
    """

    class Schema(BaseSchema):
        implicit = fields.Nested(OAuthFlow.Schema)
        password = fields.Nested(OAuthFlow.Schema)
        client_credentials = fields.Nested(OAuthFlow.Schema, load_from='clientCredentials')
        authorization_code = fields.Nested(OAuthFlow.Schema, load_from='authorizationCode')

        def represents(self):
            return OAuthFlows

    def __init__(self, implicit=None, password=None, client_credentials=None, authorization_code=None):
        self.implicit = implicit
        self.password = password
        self.client_credentials = client_credentials
        self.authorization_code = authorization_code


class SecurityScheme(BaseObject):
    """
    Defines a security scheme that can be used by the operations.
    Supported schemes are HTTP authentication, an API key (either as a
    header or as a query parameter), OAuth2's common flows (implicit,
    password, application and access code) as defined in RFC6749, and
    OpenID Connect Discovery.

    .. note:
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#securitySchemeObject
    """

    class Schema(BaseSchema):
        scheme_type = fields.Str(required=True, load_from='type')
        description = fields.Str()
        name = fields.Str()
        location = fields.Str()
        scheme = fields.Str()
        bearer_format = fields.Str(load_from='bearerFormat')
        flows = fields.Nested(OAuthFlows.Schema)
        open_id_connect_url = fields.Url(load_from='openIdConnectUrl')

        def represents(self):
            return SecurityScheme

    def __init__(self, scheme_type, description=None, name=None, location=None, scheme=None, bearer_format=None, flows=None, open_id_connect_url=None):
        self.scheme_type = scheme_type
        self.description = description
        self.name = name
        self.location = location
        self.scheme = scheme
        self.bearer_format = bearer_format
        self.flows = flows
        self.open_id_connect_url = open_id_connect_url
