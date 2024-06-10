import yaml
import json
import os
from prance import ResolvingParser
from prance.util.url import ResolutionError
from faker import Faker
import random

fake = Faker()

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
        parser = ResolvingParser(file_path, resolve_refs=True, strict=False)
        spec = parser.specification
        print("OpenAPI spec is valid.")
        return spec
    except ResolutionError as e:
        print(f"OpenAPI spec is invalid: {e}")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

def resolve_schema(schema, openapi_spec):
    if '$ref' in schema:
        ref_path = schema['$ref'].strip('#/').split('/')
        ref = openapi_spec
        try:
            for part in ref_path:
                ref = ref[part]
            return ref
        except KeyError:
            print(f"Could not resolve reference: {schema['$ref']}")
            return schema
    return schema

def generate_example_from_schema(schema, openapi_spec):
    if not schema:
        return None

    schema = resolve_schema(schema, openapi_spec)

    schema_type = schema.get('type')

    if schema_type == 'object':
        example = {}
        properties = schema.get('properties', {})
        for prop, prop_schema in properties.items():
            if prop_schema.get('format') == 'date':
                example[prop] = "{{now format='yyyy-MM-dd'}}"
            else:
                example[prop] = generate_example_from_schema(prop_schema, openapi_spec)
        return example

    elif schema_type == 'array':
        item_schema = schema.get('items')
        return [generate_example_from_schema(item_schema, openapi_spec)]

    elif schema_type == 'string':
        return schema.get('example', fake.word())

    elif schema_type == 'integer':
        return schema.get('example', random.randint(0, 100))

    elif schema_type == 'number':
        return schema.get('example', random.uniform(0, 100))

    elif schema_type == 'boolean':
        return schema.get('example', random.choice([True, False]))

    elif schema_type == 'null':
        return None

    else:
        print(f"Unknown type: {schema_type}")
        return None

def generate_wiremock_mappings(openapi_spec):
    paths = openapi_spec.get('paths', {})
    components = openapi_spec.get('definitions', {}) if 'swagger' in openapi_spec and openapi_spec['swagger'] == '2.0' else openapi_spec.get('components', {}).get('schemas', {})
    
    mappings = []
    for path, methods in paths.items():
        for method, details in methods.items():
            responses = details.get('responses', {})
            for status, response in responses.items():
                status_str = str(status)
                if status_str.startswith('2'):  # Match 2xx status codes
                    response_schema = response.get('schema', {})
                    example_response = generate_example_from_schema(response_schema, openapi_spec) if response_schema else {}
                    print(f"Generated example response for {method} {path}: {example_response}")
                    mapping = {
                        "request": {
                            "method": method.upper(),
                            "urlPath": path
                        },
                        "response": {
                            "status": int(status_str),
                            "jsonBody": example_response,
                            "transformers": ["response-template"]
                        }
                    }
                    mappings.append(mapping)
    return mappings

if __name__ == "__main__":
    file_path = 'swagger.yaml'
    openapi_spec = load_openapi_spec(file_path)
    openapi_spec = validate_openapi_spec(file_path)
    wiremock_mappings = generate_wiremock_mappings(openapi_spec)

    # Ensure the mappings directory exists
    os.makedirs('mappings', exist_ok=True)

    # Save mappings to files
    for i, mapping in enumerate(wiremock_mappings):
        with open(f'mappings/mapping_{i}.json', 'w') as file:
            json.dump(mapping, file, indent=4)

    print("Mappings generated successfully.")
