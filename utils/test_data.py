from __future__ import annotations

from pathlib import Path
from typing import Any, TypeVar

from utils.factories.reader_factory import ReaderFactory

T = TypeVar("T")


class TestData:

    @staticmethod
    def load(
        filepath: Path,
        model: type[T] | None = None,
        filters: dict | None = None,
        **kwargs: Any,
    ) -> list[T] | list[dict] | list[dict]:

        reader = ReaderFactory.get_reader(filepath)
        data = reader.read(filepath, **kwargs)

        if filters:
            data = [
                row
                for row in data
                if all(row.get(key) == value for key, value in filters.items())
            ]

        if model:

            if isinstance(data, list):
                return [model(**row) for row in data]

            return model(**data)

        return data