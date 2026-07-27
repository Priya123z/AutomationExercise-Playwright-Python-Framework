from pathlib import Path
from typing import Any

from utils.readers.reader_factory import ReaderFactory

class TestData:

    @staticmethod
    def load(
        filepath: Path,
        filters: dict | None = None,
        **kwargs: Any
    ) -> list[dict]:

        reader = ReaderFactory.get_reader(filepath)

        data = reader.read(filepath, **kwargs)

        if filters is None:
            return data

        return [
            row
            for row in data
            if all(
                row.get(key) == value
                for key, value in filters.items()
            )
        ]