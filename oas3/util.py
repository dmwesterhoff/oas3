"""
oas3.util
~~~~~~~~~
Utility functions within the library.
"""

from marshmallow.fields import Field


class RefOrSchema(Field):
    """Represents a field that should contain either a JSON reference or an Object."""

    def __init__(self, schema, **kwargs):
        super(RefOrSchema, self).__init__(**kwargs)
        self.schema = schema

    def _deserialize(self, value, attr, data):
        print(value, attr, data)
