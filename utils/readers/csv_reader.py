import csv
from pathlib import Path
from typing import Any

from utils.readers.base_reader import BaseReader


class CSVReader(BaseReader):
    """
    Reads CSV files and returns the data
    in a standardized List[Dict] format.
    """

    def validate(self,filepath: Path,**kwargs: Any) -> None:

        if not filepath.exists():
            raise FileNotFoundError(
                f"CSV file not found: {filepath}"
            )

        if filepath.suffix.lower() != ".csv":
            raise ValueError(
                f"{filepath} is not a CSV file."
            )

    def read(self,filepath: Path, **kwargs: Any) -> list[dict]:
        self.validate(filepath)
        with filepath.open(mode="r",encoding="utf-8") as csv_file:
            return self._read_rows(csv_file)

    def _read_rows(self,csv_file) -> list[dict]:
        reader = csv.DictReader(csv_file)
        return list(reader)