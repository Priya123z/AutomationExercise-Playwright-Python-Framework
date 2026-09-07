"""Read test data out of JSON, optionally as records rather than dicts.

There was a reader-per-format layer behind this once, with an abstract base
class and a factory, and the CSV and Excel branches were never exercised: there
is not a single .csv or .xlsx in the repository. Data lives in JSON, so this
reads JSON.
"""
import json


def load(filepath, model=None):
    with open(filepath, encoding="utf-8") as file:
        data = json.load(file)

    if model is None:
        return data

    # A file holds either one record or a list of them, and both shapes are in
    # use: login.json is one, payment.json is a list.
    if isinstance(data, list):
        return [model(**row) for row in data]
    return model(**data)


def append(filepath, record):
    """Append a record to a JSON list, creating the file if it is not there."""
    from dataclasses import asdict

    try:
        with open(filepath, encoding="utf-8") as file:
            existing = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing = []

    existing.append(asdict(record))
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(existing, file, indent=4)
