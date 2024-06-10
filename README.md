# Swagger to WireMock Transformer

This project transforms Swagger/OpenAPI specifications into WireMock mappings for mock API responses.

## Overview

The script `swaggerTransformer.py` reads all Swagger/OpenAPI specification files from the `swaggers` directory, validates them, and generates WireMock mapping files for mocking API responses. It supports both OpenAPI 3.0 and Swagger 2.0 specifications.

## Features

- **Supports both OpenAPI 3.0 and Swagger 2.0**: The script can process both specification formats.
- **Response Templating**: Utilizes WireMock's response templating feature to dynamically generate dates and other values.
- **Docker Integration**: Includes a Dockerfile to run WireMock with the generated mappings.

## Prerequisites

- Python 3.6 or higher
- Docker

## Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/swagger-to-wiremock-transformer.git
    cd swagger-to-wiremock-transformer
    ```

2. **Create a virtual environment and activate it**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Place your Swagger/OpenAPI specification files** (`.yaml`) in the `swaggers` directory.

2. **Run the script to generate WireMock mappings**:
    ```bash
    python swaggerTransformer.py
    ```

3. **Mappings will be generated in the `mappings` directory**.

## Testing

To run the tests:

1. **Ensure you have `unittest` installed** (comes with Python standard library).
2. **Run the test script**:
    ```bash
    python -m unittest test_swaggerTransformer.py
    ```

## Docker

### Build Docker Image

1. **Build the Docker image**:
    ```bash
    docker build -t wiremock-mappings .
    ```

2. **Run the Docker container**:
    ```bash
    docker run -p 8080:8080 wiremock-mappings
    ```

### Dockerfile

The Dockerfile included in the project performs the following actions:

- Uses the official WireMock image as the base image.
- Copies the generated `mappings` directory into the container.
- Enables response templating and verbose logging in WireMock.

## Script Details

### `swaggerTransformer.py`

This script performs the following steps:

1. **Load OpenAPI/Swagger Specification**: Reads the `.yaml` files from the `swaggers` directory.
2. **Validate Specification**: Ensures the specifications are valid using `prance`.
3. **Generate Example Responses**: Parses the specifications to generate example responses for the API endpoints.
4. **Generate WireMock Mappings**: Creates WireMock mappings with the generated responses and saves them in the `mappings` directory.

### Functions

- **load_openapi_spec(file_path)**: Loads the OpenAPI/Swagger specification from the given file path.
- **validate_openapi_spec(file_path)**: Validates the specification using `prance`.
- **resolve_schema(schema, openapi_spec)**: Resolves `$ref` references within the specification.
- **generate_example_from_schema(schema, openapi_spec)**: Generates example data based on the given schema.
- **generate_wiremock_mappings(openapi_spec)**: Generates WireMock mappings from the specification.
- **process_swagger_files()**: Processes all Swagger/OpenAPI files in the `swaggers` directory and generates mappings.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
