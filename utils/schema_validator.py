from jsonschema import validate
from pathlib import Path
import json

SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "schemas"


class SchemaValidator:

    @staticmethod
    def validate_response(response, schema_path):
        # Callers pass a path relative to schemas/, so runs no longer depend on the
        # working directory being the repo root.
        schema_file = Path(schema_path)

        if not schema_file.is_absolute():
            schema_file = SCHEMAS_DIR / schema_file

        with open(schema_file) as file:
            schema = json.load(file)

        validate(
            instance=response.json(),
            schema=schema
        )
