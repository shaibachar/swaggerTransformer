import unittest
from unittest.mock import patch, mock_open
import yaml
import json
import os
from swaggerTransformer import load_openapi_spec, validate_openapi_spec, generate_wiremock_mappings, generate_example_from_schema, process_swagger_files

class TestSwaggerTransformer(unittest.TestCase):
    
    def setUp(self):
        # Sample OpenAPI 3.0 specification
        self.sample_openapi_3_spec = """
openapi: 3.0.0
info:
  title: Customer API
  version: 1.0.0
  description: A simple API to manage customers
paths:
  /customers:
    get:
      summary: Get a list of customers
      responses:
        '200':
          description: A list of customers
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Customer'
    post:
      summary: Create a new customer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/NewCustomer'
      responses:
        '201':
          description: Customer created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Customer'
  /customers/{customerId}:
    get:
      summary: Get a customer by ID
      parameters:
        - in: path
          name: customerId
          required: true
          schema:
            type: string
      responses:
        '200':
          description: A customer
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Customer'
        '404':
          description: Customer not found
    delete:
      summary: Delete a customer by ID
      parameters:
        - in: path
          name: customerId
          required: true
          schema:
            type: string
      responses:
        '204':
          description: Customer deleted successfully
        '404':
          description: Customer not found

components:
  schemas:
    Customer:
      type: object
      properties:
        id:
          type: string
          example: "12345"
        name:
          type: string
          example: "John Doe"
        email:
          type: string
          example: "johndoe@example.com"
        phone:
          type: string
          example: "+1-555-555-5555"
        address:
          type: string
          example: "123 Main St, Anytown, USA"
        activateDate:
          type: string
          format: date
          example: "2023-06-10"
    NewCustomer:
      type: object
      required:
        - name
        - email
      properties:
        name:
          type: string
          example: "John Doe"
        email:
          type: string
          example: "johndoe@example.com"
        phone:
          type: string
          example: "+1-555-555-5555"
        address:
          type: string
          example: "123 Main St, Anytown, USA"
        activateDate:
          type: string
          format: date
          example: "2023-06-10"
"""
        # Sample Swagger 2.0 specification
        self.sample_swagger_2_spec = """
swagger: "2.0"
info:
  version: "1.0.0"
  title: "Customer API"
  description: "A simple API to manage customers"
host: "example.com"
basePath: "/"
schemes:
  - "https"
paths:
  /customers:
    get:
      summary: "Get a list of customers"
      responses:
        200:
          description: "A list of customers"
          schema:
            type: "array"
            items:
              $ref: "#/definitions/Customer"
    post:
      summary: "Create a new customer"
      parameters:
        - in: "body"
          name: "body"
          required: true
          schema:
            $ref: "#/definitions/NewCustomer"
      responses:
        201:
          description: "Customer created successfully"
          schema:
            $ref: "#/definitions/Customer"
  /customers/{customerId}:
    get:
      summary: "Get a customer by ID"
      parameters:
        - name: "customerId"
          in: "path"
          required: true
          type: "string"
      responses:
        200:
          description: "A customer"
          schema:
            $ref: "#/definitions/Customer"
        404:
          description: "Customer not found"
    delete:
      summary: "Delete a customer by ID"
      parameters:
        - name: "customerId"
          in: "path"
          required: true
          type: "string"
      responses:
        204:
          description: "Customer deleted successfully"
        404:
          description: "Customer not found"
definitions:
  Customer:
    type: "object"
    properties:
      id:
        type: "string"
        example: "12345"
      name:
        type: "string"
        example: "John Doe"
      email:
        type: "string"
        example: "johndoe@example.com"
      phone:
        type: "string"
        example: "+1-555-555-5555"
      address:
        type: "string"
        example: "123 Main St, Anytown, USA"
      activateDate:
        type: "string"
        format: "date"
        example: "2023-06-10"
  NewCustomer:
    type: "object"
    required:
      - name
      - email
    properties:
      name:
        type: "string"
        example: "John Doe"
      email:
        type: "string"
        example: "johndoe@example.com"
      phone:
        type: "string"
        example: "+1-555-555-5555"
      address:
        type: "string"
        example: "123 Main St, Anytown, USA"
      activateDate:
        type: "string"
        format: "date"
        example: "2023-06-10"
"""
        self.sample_openapi_3_spec_dict = yaml.safe_load(self.sample_openapi_3_spec)
        self.sample_swagger_2_spec_dict = yaml.safe_load(self.sample_swagger_2_spec)
    
    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_load_openapi_spec(self, mock_file):
        with patch('yaml.safe_load', return_value=self.sample_openapi_3_spec_dict):
            spec = load_openapi_spec("swagger.yaml")
            self.assertEqual(spec, self.sample_openapi_3_spec_dict)
    
    @patch("swaggerTransformer.ResolvingParser")
    def test_validate_openapi_spec(self, mock_resolving_parser):
        mock_parser_instance = mock_resolving_parser.return_value
        mock_parser_instance.specification = self.sample_openapi_3_spec_dict
        spec = validate_openapi_spec("swagger.yaml")
        self.assertEqual(spec, self.sample_openapi_3_spec_dict)
    
    def test_generate_example_from_schema_openapi_3(self):
        customer_schema = self.sample_openapi_3_spec_dict['components']['schemas']['Customer']
        example = generate_example_from_schema(customer_schema, self.sample_openapi_3_spec_dict)
        self.assertIn('id', example)
        self.assertIn('name', example)
        self.assertIn('email', example)
        self.assertIn('phone', example)
        self.assertIn('address', example)
        self.assertIn('activateDate', example)
    
    def test_generate_example_from_schema_swagger_2(self):
        customer_schema = self.sample_swagger_2_spec_dict['definitions']['Customer']
        example = generate_example_from_schema(customer_schema, self.sample_swagger_2_spec_dict)
        self.assertIn('id', example)
        self.assertIn('name', example)
        self.assertIn('email', example)
        self.assertIn('phone', example)
        self.assertIn('address', example)
        self.assertIn('activateDate', example)

    def test_generate_wiremock_mappings_openapi_3(self):
        mappings = generate_wiremock_mappings(self.sample_openapi_3_spec_dict)
        self.assertEqual(len(mappings), 4)
        for mapping in mappings:
            self.assertIn('request', mapping)
            self.assertIn('response', mapping)
            self.assertIn('jsonBody', mapping['response'])

    def test_generate_wiremock_mappings_swagger_2(self):
        mappings = generate_wiremock_mappings(self.sample_swagger_2_spec_dict)
        self.assertEqual(len(mappings), 4)
        for mapping in mappings:
            self.assertIn('request', mapping)
            self.assertIn('response', mapping)
            self.assertIn('jsonBody', mapping['response'])

    @patch('swaggerTransformer.glob.glob', return_value=['swaggers/swagger1.yaml', 'swaggers/swagger2.yaml'])
    @patch('swaggerTransformer.load_openapi_spec')
    @patch('swaggerTransformer.validate_openapi_spec')
    @patch('swaggerTransformer.generate_wiremock_mappings')
    def test_process_swagger_files(self, mock_generate_mappings, mock_validate_spec, mock_load_spec, mock_glob):
        mock_load_spec.return_value = self.sample_openapi_3_spec_dict
        mock_validate_spec.return_value = self.sample_openapi_3_spec_dict
        mock_generate_mappings.return_value = [{"request": {}, "response": {}}]

        process_swagger_files()
        mock_glob.assert_called_with('swaggers/*.yaml')
        self.assertTrue(os.path.exists('mappings'))

if __name__ == '__main__':
    unittest.main()
