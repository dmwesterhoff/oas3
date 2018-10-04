"""
oas3.base
~~~~~~~~~
Implements base classes for internal inheritance within the API.
"""

import pathlib
import json
import yaml
import requests
import marshmallow
from inspect import cleandoc
from marshmallow import post_dump, post_load
from .errors import ValidationError, LoadingError, DumpingError


class BaseSchema(marshmallow.Schema):
    """Provides a base schema for all OAS3 object schemas to inherit from."""
    def represents(self):
        """All OAS3 object schemas must implement this method to act
        as a reference to the class the schema represents."""
        raise NotImplementedError()

    @post_dump
    def skip_none_values(self, data):
        """Skips any values that are None because they were not provided."""
        return {
            key: value for key, value in data.items()
            if value is not None
        }

    @post_load
    def make_obj(self, data):
        return self.represents()(**data)


class BaseObject:
    """Provides a base class for all OAS3 objects to inherit from."""

    @classmethod
    def from_file(cls, path):
        """
        Reads in a file from a system path to load a spec object.

        :param path: An absolute or local path to the file to be loaded
        :returns instance: Newly created object of the same type the method
            was called from

        Example:
            >>> from oas3 import Spec
            >>> spec = Spec.from_file('./tests/samples/valid/uspto.yaml')
        """
        data = open(path).read()
        extension = pathlib.Path(path).suffix
        if extension == '.json':
            return cls.from_json(data)
        if extension in ['.yaml', '.yml']:
            return cls.from_yaml(data)
        return cls.from_raw(data)

    @classmethod
    def from_url(cls, url, format_type=None):
        """
        Load a JSON or YAML OAS 3 spec object from a provided url string.

        :param url: The endpoint where the file is hosted at.
        :param format_type: either `json` or `yaml` or None, if  None it will attempt
        to be inferred.
        :returns instance: a newly created object or the type this method was called from

        Example:
            >>> from oas3 import Spec
            >>> spec = Spec.from_url('https://raw.githubusercontent.com/OAI/OpenAPI-Specification/master/examples/v3.0/petstore.yaml')
        """
        response = requests.get(url)
        if not response.ok:
            raise LoadingError('HTTP Error: {}'.format(response.status_code))
        if format_type == 'yaml':
            return cls.from_yaml(response.text)
        elif format_type == 'json':
            return cls.from_json(response.text)
        else:
            return cls.from_raw(response.text)

    @classmethod
    def from_dict(cls, dictionary):
        """
        Load the object with a python dictionary.

        :returns instance: Returns a newly created instance of the class this method
            was called from.
        :raises ValidationError: Raises if the data doesnt meet object defined schema.
        """
        result, errors = cls.Schema().load(dictionary)
        if errors:
            raise ValidationError("Validation error encountered in [{}] ".format(cls.__name__) +
                                  str(errors))
        return result

    @classmethod
    def from_json(cls, json_string):
        """
        Loads the OAS3 object with a JSON string.

        :returns instance: Returns a newly created instance of the class this method
            was called from.
        :raises ValidationError: Raises if JSON is invalid or if the specification
            data was invalid.
        """
        try:
            dictionary = json.loads(json_string)
        except:
            raise ValidationError('Unable to load, invalid JSON data')
        return cls.from_dict(dictionary)

    @classmethod
    def from_yaml(cls, yaml_string):
        """
        Loads the OAS3 object with a YAML string.

        :returns instance: Returns a newly created instance of the class this method
            was called from.
        :raises ValidationError: Raises if YAML is invalid or if the specification
            data was invalid.
        """
        try:
            dictionary = yaml.load(yaml_string)
        except:
            raise ValidationError('Unable to load, invalid YAML data')
        return cls.from_dict(dictionary)

    @classmethod
    def from_docstring(cls, obj_or_cls_or_func):
        """
        Load the OAS3 objects with the docstring of a class, object, or method.

        :returns instance: Returns a newly created instance of the class this method
            was called from.
        :raises ValidationError: Raises if data in docstring is invalid YAML or JSON,
            if the specification data was invalid, or the passed variable doesnt have
            a docstring.
        """
        if obj_or_cls_or_func.__doc__ is None:
            raise ValidationError('Attemped to load docstring but it was None')
        docstring = cleandoc(obj_or_cls_or_func.__doc__)
        return cls.from_raw(docstring)

    @classmethod
    def from_raw(cls, data):
        """
        This loader will attempt to load either JSON or YAML data, it should only
        be used if the data type is unknown at runtime, otherwise from_json() or
        from_yaml() should be used.

        :returns instance: Returns a newly created instance of the class this method
            was called from.
        :raises ValidationError: Raises if data doesnt appear to be YAML or JSON,
            or if the specification data contained is invalid.
        """
        try:
            return cls.from_yaml(data)
        except Exception as e:
            print(str(e))
        try:
            return cls.from_json(data)
        except Exception as e:
            print(str(e))
        raise ValidationError('Unable to detect valid JSON or YAML in data.')

    def to_dict(self):
        """
        Converts all subattributes to python builtin data types so that the
        OAS3 object can be represented as a dict.

        :returns dict: A dictionary representation of the OAS3 object
        :raises ValidationError: if serializing the data was unsuccessful.
        """
        data, errors = self.Schema().dump(self)
        if errors:
            raise ValidationError(errors)
        errors = self.Schema().validate(data)
        if errors:
            raise ValidationError(errors)
        return data

    def to_json(self, pretty=True, indent=2):
        """
        Converts the OAS3 object into a JSON string.

        :param pretty: If True the JSON output will be indented, sorted and nicely
            separated.
        :param indent: Ignored unless pretty=True, number of spaces to indent output
        :returns str: A JSON string of the OAS3 object
        :raises ValidationError: if serializing the data was unsuccessful.
        """
        if pretty:
            return json.dumps(self.to_dict(),
                              indent=indent,
                              sort_keys=True,
                              separators=(',', ': '))
        return json.dumps(self.to_dict())

    def to_yaml(self):
        """
        Converts the OAS3 object into a YAML string.

        :returns str: A YAML string of the OAS3 object
        :raises ValidationError: if serializing the data was unsuccessful.
        """
        return yaml.dump(self.to_dict(), default_flow_style=False)

    def to_file(self, path, format_type=None):
        file_ref = open(path, 'w')
        extension = pathlib.Path(path).suffix
        if format_type:
            extension = '.' + format_type

        if extension == '.json':
            file_ref.write(self.to_json())
            file_ref.close()
        elif extension in ['.yaml', '.yml']:
            file_ref.write(self.to_yaml())
            file_ref.close()
        else:
            raise DumpingError('Unable to determine format to save data, \
                                please specify a `format_type` if a proper file \
                                extension is not given')
        return

    def is_valid(self):
        """
        Determines if the loaded data into the OAS3 object appears to be valid,
        note that this method cannot determine the overall validity because its
        scope is limited to itself. So for example its impossible to validate
        local refs with this method.

        :returns bool: True if the object is valid in its scheme, False otherwise
        """
        data, errors = self.Schema().dump(self)
        if errors:
            return False
        errors = self.Schema().validate(data)
        if errors:
            return False
        return True
