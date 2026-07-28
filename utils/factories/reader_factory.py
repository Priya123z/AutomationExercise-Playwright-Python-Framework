from utils.readers.csv_reader import CSVReader
from utils.readers.excel_reader import ExcelReader
from utils.readers.json_reader import JSONReader
from pathlib import Path


class ReaderFactory:

    _READERS = {
        ".csv": CSVReader,
        ".xlsx": ExcelReader,
        ".xls": ExcelReader,
        ".json": JSONReader,
    }

    @staticmethod
    def get_reader(filepath: Path):

        extension = filepath.suffix.lower()

        reader = ReaderFactory._READERS.get(extension)

        if reader is None:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        return reader()