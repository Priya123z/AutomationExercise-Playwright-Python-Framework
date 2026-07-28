import json
from dataclasses import asdict
from json import JSONDecodeError
from pathlib import Path

from utils.writers.base_writer import BaseWriter


class JsonWriter(BaseWriter):

    def write(self, file_path: Path, data):

        with open(file_path, "w") as file:
            json.dump(asdict(data), file, indent=4)

    def append(self, file_path, data):

        try:
            with open(file_path, "r") as file:
                existing = json.load(file)

        except (FileNotFoundError, JSONDecodeError):
            existing = []

        existing.append(asdict(data))

        with open(file_path, "w") as file:
            json.dump(existing, file, indent=4)