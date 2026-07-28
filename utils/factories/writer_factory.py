from utils.writers.csv_writer import CsvWriter
from utils.writers.json_writer import JsonWriter


class WriterFactory:

    @staticmethod
    def get_writer(file_path):

        suffix = file_path.suffix.lower()

        if suffix == ".json":
            return JsonWriter()

        if suffix == ".csv":
            return CsvWriter()

        raise ValueError(f"Unsupported file type: {suffix}")