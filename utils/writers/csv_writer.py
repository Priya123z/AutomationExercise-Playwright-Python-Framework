import csv
from dataclasses import asdict

from utils.writers.base_writer import BaseWriter


class CsvWriter(BaseWriter):

    def write(self, file_path, data):

        values = asdict(data)

        with open(file_path, "w", newline="") as file:

            writer = csv.DictWriter(file, fieldnames=values.keys())

            writer.writeheader()

            writer.writerow(values)

    def append(self, file_path, data):

        values = asdict(data)

        file_exists = file_path.exists()

        with open(file_path, "a", newline="") as file:

            writer = csv.DictWriter(file, fieldnames=values.keys())

            if not file_exists:
                writer.writeheader()

            writer.writerow(values)