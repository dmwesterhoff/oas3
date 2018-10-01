.. |travis-ci| image:: https://img.shields.io/travis/pinntech/oas3/master.svg?style=flat-square
    :target: https://travis-ci.org/#!/pinntech/oas3?branch=master
.. |coveralls| image:: https://img.shields.io/coveralls/pinntech/oas3/master.svg?style=flat-square
    :target: https://coveralls.io/r/pinntech/oas3?branch=master
.. |pypi| image:: https://img.shields.io/pypi/v/oas3.svg?style=flat-square
    :target: https://pypi.python.org/pypi/oas3
.. |license| image:: https://img.shields.io/pypi/l/oas3.svg?style=flat-square
    :target: https://pypi.python.org/pypi/oas3

****
OAS3
****
|travis-ci| |coveralls| |pypi| |license| 

OAS3 is a parser, validator and compiler for dealing with Open API
Specification v3. This library provides an interface for working with
specifications, and loading and dumping to various locations and formats.

Quickstart
===========

To get started load your spec, it will be validated upon dumping.

.. code-block:: python

   from oas3 import Spec

   # Load the Spec from a file
   spec = Spec.from_file('./spec.json')
   spec = Spec.from_file('./spec.yml')

   # Load the Spec from a URL
   spec = Spec.from_url('https://raw.githubusercontent.com/OAI/OpenAPI-Specification/master/examples/v3.0/petstore.yaml')

   # Load the Spec from a python native dictionary
   spec = Spec.from_dict(spec_dict)

   # A spec that is sufficiently loaded (i.e. valid OAS3) can now be dumped
   spec.to_file('/tmp/spec.yaml')
   spec.to_dict()
   spec.to_json()
   spec.to_yaml()
