import json
from typing import Any

import pytest

from utils.readers.base_reader import BaseReader


class JSONReader(BaseReader):
    def read(self, filepath, **kwargs):
        self.validate(filepath, **kwargs)

        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        return [pytest.param(value, id=name) for name, value in data.items()]

    def validate(self, filepath, **kwargs:Any)->None:
        if not filepath.exists():
            raise FileNotFoundError(f"{filepath} does not exist")

        if filepath.suffix.lower() != ".json":
            raise ValueError(f"{filepath} is not a json file")


