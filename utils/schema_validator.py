from jsonschema import validate
from pathlib import Path
import json


class SchemaValidator:

    @staticmethod
    def validate_response(response, schema_path):

        with open(schema_path) as file:
            schema = json.load(file)

        validate(
            instance=response.json(),
            schema=schema
        )