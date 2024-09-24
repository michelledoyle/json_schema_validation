Introduction
The JSON Validation Service is a Django-based RESTful API that validates incoming JSON messages against a predefined schema using the jsonschema framework. It ensures JSON data conforms to the expected structure, returning validation status and detailed error messages when necessary.
Key Features:
Accepts JSON via HTTPS POST requests.
Validates JSON using jsonschema.
Returns validation status and error details.
Technologies:
Django
Django REST Framework (DRF)
jsonschema library

Base URL
Local Development: http://localhost:8000/json-validate/
sandbox: https://json-validator-service-956921068659.us-central1.run.app/json-validate/

Request Details
Endpoint
POST /validate-json/
Description: Validates the submitted JSON data against the predefined schema.
Headers
Content-Type: application/json
(Optional) X-API-Key: the API key if authentication is enabled.
Authentication
Optional: If the service requires API key authentication, include the X-API-Key header in the request.
Example:
bash

-H "X-API-Key: the-secret-api-key"

Request Body
The request body must be a JSON object that conforms to the schema defined in the service.
The JSON should be sent in the body of the request as raw JSON.

JSON Schema Overview
The expected JSON structure is defined by the schema in schema.json.
json

{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "PatientData",
  "type": "object",
  "properties": {
    "Patient": {
      "type": "object",
      "properties": {
        "Info": {
          "type": "object",
          "properties": {
            "PatientBk": {
              "type": "string",
              "maxLength": 128
            },
            "FirstNm": {
              "type": "string",
              "maxLength": 100
            },
            "LastNm": {
              "type": "string",
              "maxLength": 100
            },
            "PatientId": {
              "type": "string",
              "maxLength": 128
            },
            "ActiveInd": {
              "type": "string",
              "enum": ["Y", "N"]
            }
            // ... other optional properties ...
          },
          "required": ["PatientBk"]
        },
        "Address": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "ActiveInd": {
                "type": "string",
                "enum": ["Y", "N"]
              },
              "AddressType": {
                "type": "string",
                "maxLength": 50
              },
              "AddressUse": {
                "type": "string",
                "maxLength": 50
              },
              "AddressLine1Descr": {
                "type": "string",
                "maxLength": 255
              },
              "CityNm": {
                "type": "string",
                "maxLength": 100
              },
              "StateProvinceCd": {
                "type": "string",
                "maxLength": 50
              },
              "PostalCd": {
                "type": "string",
                "maxLength": 20
              },
              "CountryNm": {
                "type": "string",
                "maxLength": 100
              }
              // ... other optional properties ...
            },
            "required": ["ActiveInd", "AddressType", "AddressUse", "AddressLine1Descr", "CityNm", "StateProvinceCd", "PostalCd", "CountryNm"]
          }
        }
        // ... other optional sections like Identification, Phone, Email ...
      },
      "required": ["Info"]
    }
  },
  "required": ["Patient"]
}

Key Required Fields
Patient
Info
PatientBk (string, maxLength: 128)
Other fields are optional but must adhere to the types and constraints specified if included.

Response Details
Successful Validation
Status Code: 200 OK
Response Body:
json

{
  "status": "success",
  "message": "JSON is valid."
}


Validation Error
Status Code: 400 Bad Request
Response Body:
json

{
  "status": "error",
  "message": "JSON validation error: <error_message>",
  "path": ["<path_to_error>"]
}
<error_message>: A descriptive message explaining why the validation failed.
<path_to_error>: An array indicating the location within the JSON where the error occurred.
Other Errors
Status Code: 500 Internal Server Error
Response Body:
json

{
  "status": "error",
  "message": "An unexpected error occurred: <error_message>"
}


Examples
1. Valid JSON Example
Request
bash

curl -X POST https://json-validator-service-956921068659.us-central1.run.app/json-validate/ \
  -H "Content-Type: application/json" \
  -d '{
    "Patient": {
      "Info": {
        "PatientBk": "PBK123456",
        "FirstNm": "John",
        "LastNm": "Doe",
        "PatientId": "P0001",
        "ActiveInd": "Y"
      },
      "Address": [
        {
          "ActiveInd": "Y",
          "AddressType": "Home",
          "AddressUse": "Primary",
          "AddressLine1Descr": "123 Main St",
          "CityNm": "Springfield",
          "StateProvinceCd": "IL",
          "PostalCd": "62704",
          "CountryNm": "USA"
        }
      ]
    }
  }'

Response
json

{
  "status": "success",
  "message": "JSON is valid."
}


2. Invalid JSON Example: Missing Required Field
Request
bash

curl -X POST https://json-validator-service-956921068659.us-central1.run.app/json-validate/ \
  -H "Content-Type: application/json" \
  -d '{
    "Patient": {
      "Info": {
        "FirstNm": "John",
        "LastNm": "Doe",
        "PatientId": "P0001",
        "ActiveInd": "Y"
      },
      "Address": [
        {
          "ActiveInd": "Y",
          "AddressType": "Home",
          "AddressUse": "Primary",
          "AddressLine1Descr": "123 Main St",
          "CityNm": "Springfield",
          "StateProvinceCd": "IL",
          "PostalCd": "62704",
          "CountryNm": "USA"
        }
      ]
    }
  }'

Response
json

{
  "status": "error",
  "message": "JSON validation error: 'PatientBk' is a required property",
  "path": ["Patient", "Info"]
}


3. Invalid JSON Example: Incorrect Data Type
Request
bash

curl -X POST https://json-validator-service-956921068659.us-central1.run.app/json-validate/ \
  -H "Content-Type: application/json" \
  -d '{
    "Patient": {
      "Info": {
        "PatientBk": "PBK123456",
        "FirstNm": "John",
        "LastNm": "Doe",
        "PatientId": "P0001",
        "ActiveInd": true  // Should be "Y" or "N"
      },
      "Address": [
        {
          "ActiveInd": "Y",
          "AddressType": "Home",
          "AddressUse": "Primary",
          "AddressLine1Descr": "123 Main St",
          "CityNm": "Springfield",
          "StateProvinceCd": "IL",
          "PostalCd": "62704",
          "CountryNm": "USA"
        }
      ]
    }
  }'

Response
json

{
  "status": "error",
  "message": "JSON validation error: True is not of type 'string'",
  "path": ["Patient", "Info", "ActiveInd"]
}


4. Invalid JSON Example: Missing Required Section
Request
bash

curl -X POST https://json-validator-service-956921068659.us-central1.run.app/json-validate/ \
  -H "Content-Type: application/json" \
  -d '{
    "Patient": {}
  }'

Response
json

{
  "status": "error",
  "message": "JSON validation error: 'Info' is a required property",
  "path": ["Patient"]
}


5. Valid JSON Example: Minimal Required Fields
Request
bash

curl -X POST https://json-validator-service-956921068659.us-central1.run.app/json-validate/ \
  -H "Content-Type: application/json" \
  -d '{
    "Patient": {
      "Info": {
        "PatientBk": "PBK123456"
      }
    }
  }'

Response
json

{
  "status": "success",
  "message": "JSON is valid."
}


Error Handling
Possible Error Responses
400 Bad Request: The JSON data is invalid or does not conform to the schema.
401 Unauthorized: Missing or invalid API key (if authentication is enabled).
429 Too Many Requests: Rate limit exceeded (if rate limiting is enabled).
500 Internal Server Error: An unexpected error occurred on the server.
Common Error Messages
No JSON data provided: The request body is empty or not valid JSON.
JSON validation error: The JSON does not conform to the schema; details provided in the message.
Schema file not found: The server could not locate the schema file.
An unexpected error occurred: A generic error message for unhandled exceptions.

Headers
Request Headers
Content-Type: Must be set to application/json.
X-API-Key: the API key for authentication.
Response Headers
Content-Type: application/json

Authentication
If API key authentication is enabled, you must include the X-API-Key header in the request.
Including API Key in Request
bash

-H "X-API-Key: the-secret-api-key"

Example Request with Authentication
bash

curl -X POST https://json-validator-service-956921068659.us-central1.run.app/json-validate/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: the-secret-api-key" \
  -d '{ ... }'

Response for Invalid API Key
json

{
  "detail": "Invalid API key."
}