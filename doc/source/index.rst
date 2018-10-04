****
OAS3
****
.. currentmodule:: oas3

Usage
=====

Installation
------------

::

   pip install oas3

Quick start
-----------

Loading the `Spec` object from various sources:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from oas3 import Spec

   # Load the Spec from a file
   spec = Spec.from_file('./spec.json')
   spec = Spec.from_file('./spec.yml')

   # Load the Spec from a URL
   spec = Spec.from_url('https://raw.githubusercontent.com/OAI/OpenAPI-Specification/master/examples/v3.0/petstore.yaml')

   # Load the Spec from a python native dictionary
   spec = Spec.from_dict(spec_dict)

   # Or from JSON or YAML strings
   spec = Spec.from_json(json_string)
   spec = Spec.from_yaml(yaml_string)

If loading is successful, that means the spec was properly validated and is ready
to use. During this process if anything goes wrong with validation a `oas3.ValidationError`
will be raised.

Dumping the `Spec` object to various destinations:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python
 
   from oas3 import Spec

   spec = Spec.from_file('./spec.json')
   spec.to_json()
   #
   spec.to_yaml()
   #
   spec.to_file()
   #
   spec.to_dict()

Composing a Spec
----------------
The OAS3 has the ability for you to compose specification in python natively,
unlike the standard loaders the composed spec will not be validated unless
spec.validate() or you try and dump the spec object.

Spec object basics
~~~~~~~~~~~~~~~~~~
   
.. code-block:: python

   import oas3

   # Create an empty spec
   spec = oas3.Spec()

   # Load a Spec Object up
   info = oas3.Info(version='0.1.0', title='Petstore')
   # ... load more objects

   # Insert it into the specification
   spec.info = info

   # Validate it whenever you want
   spec.is_valid()
   # False
   
   info.is_valid()
   # True

   # Dump it when your ready
   json_string = spec.to_json()

Component loading
~~~~~~~~~~~~~~~~~~
   
.. code-block:: python

   import oas3

   # These are all equivalent
   info = oas3.Info(version='0.1.0', title='Petstore')
   info = oas3.Info.from_dict({'version': '0.1.0', 'title': 'Petstore'})
   class Info:
       """
       version: 1.0.0
       title: Petstore
       """
   info = oas3.Info.from_docstring(Info)

API
===

Core
----
.. autoclass:: oas3.base.BaseObject
.. autoclass:: oas3.Spec

Exceptions
----------
.. autoexception:: ValidationError

Utils
-----

.. automodule:: oas3.util


.. include:: ../../HISTORY.rst

References
==========
* `Open API Specification v3 <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#responseObject>`_
