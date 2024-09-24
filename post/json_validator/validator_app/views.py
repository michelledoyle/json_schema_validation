# validator_app/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from jsonschema import validate, ValidationError, SchemaError
import json
import os
from django.conf import settings

class ValidateJSONView(APIView):
    """
    API endpoint that allows JSON validation against a predefined schema.
    """

    def post(self, request, format=None):
        # Path to the JSON schema file
        schema_path = os.path.join(settings.BASE_DIR, 'validator_app', 'schema.json')

        # Load the JSON schema
        try:
            with open(schema_path, 'r') as schema_file:
                schema = json.load(schema_file)
        except FileNotFoundError:
            return Response(
                {"status": "error", "message": "Schema file not found."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except json.JSONDecodeError as e:
            return Response(
                {"status": "error", "message": f"Invalid JSON schema: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Get JSON data from request
        data = request.data

        # Validate that data is provided
        if not data:
            return Response(
                {"status": "error", "message": "No JSON data provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate the JSON data against the schema
        try:
            validate(instance=data, schema=schema)
        except ValidationError as ve:
            # Extract the error path for better error messages
            error_path = list(ve.path)
            return Response(
                {
                    "status": "error",
                    "message": f"JSON validation error: {ve.message}",
                    "path": error_path
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except SchemaError as se:
            return Response(
                {"status": "error", "message": f"Schema error: {se.message}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {"status": "error", "message": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # If validation passes
        return Response(
            {"status": "success", "message": "JSON is valid."},
            status=status.HTTP_200_OK
        )
