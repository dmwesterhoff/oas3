"""
oas3.errors
~~~~~~~~~~~
Defines custom pacakage specific exceptions.
"""

class ValidationError(Exception):
    pass


class LoadingError(Exception):
    pass


class DumpingError(Exception):
    pass
