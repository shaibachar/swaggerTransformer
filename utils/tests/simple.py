import yaml
from prance import ResolvingParser
from prance.util.url import ResolutionError

def load_openapi_spec(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            openapi_spec = yaml.safe_load(file)
        return openapi_spec
    except Exception as e:
        print(f"Failed to load the OpenAPI spec: {e}")
        exit(1)

def validate_openapi_spec(file_path):
    try:
        parser = ResolvingParser(file_path)
        spec = parser.specification
        print("OpenAPI spec is valid.")
        return spec
    except ResolutionError as e:
        print(f"OpenAPI spec is invalid: {e}")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    file_path = '/home/shai/workspace/swaggerTransformer/utils/tests/swagger.yaml'
    openapi_spec = load_openapi_spec(file_path)
    print("Loaded OpenAPI spec:")
    print(openapi_spec)
    validate_openapi_spec(file_path)
