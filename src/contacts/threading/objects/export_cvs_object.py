import csv
from typing import Any

from PyQt6.QtCore import QObject, pyqtSignal

from src.utilities.encoding_provider import get_encoding


class ExportCsvObject(QObject):
    error_message = pyqtSignal(Exception)
    finished = pyqtSignal(bool)
    def __init__(self, file_path: str, headers: list, delimiter: str, csv_data: list[dict[str, Any]]) -> None:
        super().__init__()
        self.file_path = file_path
        self.headers = headers
        self.delimiter = delimiter
        self.csv_data = csv_data

    def run_csv_export(self) -> None:
        try:
            with open(self.file_path, "w", newline="", encoding=get_encoding()) as file:
                writer = csv.DictWriter(file, fieldnames=self.headers, delimiter=self.delimiter)
                writer.writeheader()
                writer.writerows(self.csv_data)
                self.finished.emit(True)
        except Exception as e:
            self.error_message.emit(e)
            self.finished.emit(False)