from typing import TYPE_CHECKING
import csv

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMainWindow

from src.utilities.encoding_provider import get_encoding

if TYPE_CHECKING:
    from src.database.utilities.contacts_utilities.export_data_provider import ExportDataProvider


# noinspection PyUnresolvedReferences
class ExportCsvObject(QObject):
    error_message = pyqtSignal(Exception)
    finished = pyqtSignal(bool)
    def __init__(self, db_path: str, file_path: str, id_list: list | None, export_data_provider: "ExportDataProvider",
                 main_window: QMainWindow) -> None:
        super().__init__()
        self.db_path = db_path
        self.file_path = file_path
        self.id_list = id_list
        self.export_data_provider = export_data_provider
        self.main_window = main_window
        self.connection_name = f"exportCsvThread{id(self)}"

    def run_csv_export(self) -> None:
        db_connection = None
        try:
            db_connection = QSqlDatabase.addDatabase("QSQLITE", self.connection_name)
            db_connection.setDatabaseName(self.db_path)
            if not db_connection.open():
                self.finished.emit(False)
                return
            semicolon, headers, csv_data = self.export_data_provider.get_csv_data(db_connection, self.id_list,
                                                                                  self.main_window)
            if not semicolon or not headers or not csv_data:
                self.finished.emit(False)
                return
            delimiter = ","
            if semicolon:
                delimiter = ";"
            with open(self.file_path, "w", newline="", encoding=get_encoding()) as file:
                writer = csv.DictWriter(file, fieldnames=headers, delimiter=delimiter)
                try:
                    writer.writeheader()
                    writer.writerows(csv_data)
                except Exception as e:
                    self.error_message.emit(e)
                    self.finished.emit(False)
                    return
            self.finished.emit(True)
        except Exception as e:
            self.error_message.emit(e)
            self.finished.emit(False)
        finally:
            if db_connection:
                db_connection.close()
                del db_connection
            QSqlDatabase.removeDatabase(self.connection_name)