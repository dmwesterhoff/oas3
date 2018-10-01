"""
oas3.primitives
~~~~~~~~~~~~~~~
Defines OAS3 enumerated primitive values.
"""


class INTEGER:
    COMMON_NAME = "integer"
    TYPE = "INTEGER"
    FORMAT = "int32"


class LONG:
    COMMON_NAME = "integer"
    TYPE = "INTEGER"
    FORMAT = "int64"


class FLOAT:
    COMMON_NAME = "float"
    TYPE = "number"
    FORMAT = "float"


class DOUBLE:
    COMMON_NAME = "double"
    TYPE = "number"
    FORMAT = "double"


class STRING:
    COMMON_NAME = "string"
    TYPE = "string"
    FORMAT = None


class BYTE:
    COMMON_NAME = "byte"
    TYPE = "string"
    FORMAT = "byte"


class BINARY:
    COMMON_NAME = "binary"
    TYPE = "string"
    FORMAT = "binary"


class BOOLEAN:
    COMMON_NAME = "boolean"
    TYPE = "boolean"
    FORMAT = None


class DATE:
    COMMON_NAME = "date"
    TYPE = "string"
    FORMAT = "date"


class DATETIME:
    COMMON_NAME = "dateTime"
    TYPE = "string"
    FORMAT = "date-time"


class PASSWORD:
    COMMON_NAME = "password"
    TYPE = "string"
    FORMAT = "password"
