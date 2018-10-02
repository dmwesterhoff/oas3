from oas3 import Spec, Path


def test_import():
    import oas3


def test_module_version():
    import oas3
    assert oas3.__version__ is not None


def test_spec_from_file():
    Spec.from_file('./tests/samples/valid/uspto.yaml')


def test_specs():
    Spec.from_file('./tests/samples/valid/api-with-examples.yaml')
    Spec.from_file('./tests/samples/valid/link-example.yaml')
    Spec.from_file('./tests/samples/valid/petstore-expanded.yaml')
    Spec.from_file('./tests/samples/valid/petstore.yaml')
    Spec.from_file('./tests/samples/valid/uspto.yaml')

def pets():
    """
    get:
      summary: List all pets
      operationId: listPets
      tags:
        - pets
      parameters:
        - name: limit
          in: query
          description: How many items to return at one time (max 100)
          required: false
          schema:
            type: integer
            format: int32
      responses:
        '200':
          description: A paged array of pets
          headers:
            x-next:
              description: A link to the next page of responses
              schema:
                type: string
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Pets"
        default:
          description: unexpected error
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
    """
    pass


def test_load_path_docstring():
    path = Path.from_docstring(pets)


def test_from_url_json():
    pass


def test_from_url_yaml():
    pass


def test_from_file_json():
    pass


def test_from_file_yaml():
    pass


def test_spec_conversions():
    from oas3 import Spec
    spec = Spec.from_url('https://raw.githubusercontent.com/OAI/OpenAPI-Specification/master/examples/v3.0/petstore.yaml')
    spec = Spec.from_dict(spec.to_dict())
    spec = Spec.from_json(spec.to_json())
    spec = Spec.from_yaml(spec.to_yaml())
