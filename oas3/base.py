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
    """
    """
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
    """
    """

    @classmethod
    def from_file(cls, path):
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
        Load a JSON or YAML OAS 3 specification from a provided url string.

        :param url: The endpoint where the file is hosted at.
        :param format_type: either `json` or `yaml`
        :returns Spec: a newly created Spec object

        Example:
            >>> from oas3 import Spec
            >>> spec = Spec.from_url('https://raw.githubusercontent.com/OAI/OpenAPI-Specification/master/examples/v3.0/petstore.yaml', format_type='yaml')
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
        result, errors = cls.Schema().load(dictionary)
        if errors:
            raise ValidationError("Validation error encountered in [{}] ".format(cls.__name__) +
                                  str(errors))
        return result

    @classmethod
    def from_json(cls, json_string):
        try:
            dictionary = json.loads(json_string)
        except:
            raise ValidationError('Unable to load, invalid JSON data')
        return cls.from_dict(dictionary)

    @classmethod
    def from_yaml(cls, yaml_string):
        try:
            dictionary = yaml.load(yaml_string)
        except:
            raise ValidationError('Unable to load, invalid YAML data')
        return cls.from_dict(dictionary)

    @classmethod
    def from_docstring(cls, obj_or_cls):
        docstring = cleandoc(obj_or_cls.__doc__)
        return cls.from_raw(docstring)

    @classmethod
    def from_raw(cls, data):
        try:
            return cls.from_yaml(data)
        except Exception as e:
            print(e)
            return
        try:
            return cls.from_json(data)
        except:
            print(e)
            return
        raise ValidationError('Unable to detect valid JSON or YAML in data.')

    def to_dict(self):
        data, errors = self.Schema().dump(self)
        if errors:
            raise ValidationError(errors)
        errors = self.Schema().validate(data)
        if errors:
            raise ValidationError(errors)
        return data

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_yaml(self):
        return yaml.dump(self.to_dict(), default_flow_style=False)

    def to_file(self, path, format_type=None):
        f = open(path, 'w')
        extension = pathlib.Path(path).suffix
        if format_type:
            extension = '.' + format_type

        if extension == '.json':
            f.write(self.to_json())
            f.close()
        elif extension in ['.yaml', '.yml']:
            f.write(self.to_yaml())
            f.close()
        else:
            raise DumpingError('Unable to determine format to save data, please specify a `format_type` if a proper file extension is not given')
        return

    def is_valid(self):
        data, errors = self.Schema().dump(self)
        if errors:
            return False
        errors = self.Schema().validate(data)
        if errors:
            return False
        return True
