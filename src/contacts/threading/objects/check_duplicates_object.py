from typing import TYPE_CHECKING

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMainWindow

if TYPE_CHECKING:
    from src.database.utilities.contacts_utilities.query_provider import QueryProvider


# noinspection PyUnresolvedReferences
class CheckDuplicatesObject(QObject):
    error_message = pyqtSignal(Exception)
    finished = pyqtSignal(list)
    def __init__(self, db_path: str, query_provider: "QueryProvider", main_window: QMainWindow) -> None:
        super().__init__()
        self.setObjectName("checkDuplicatesObject")
        self.db_path = db_path
        self.query_provider = query_provider
        self.main_window= main_window
        self.connection_name = f"checkDuplicatesThread{id(self)}"

    def run_check_duplicates(self) -> None:
        db_connection = None
        self.selected_contacts = []
        try:
            db_connection = QSqlDatabase.addDatabase("QSQLITE", self.connection_name)
            db_connection.setDatabaseName(self.db_path)
            if not db_connection.open():
                self.finished.emit(self.selected_contacts)
                return
            self.selected_contacts = self.query_provider.create_check_duplicates_query(db_connection, self.main_window)
            if not self.selected_contacts:
                self.finished.emit(self.selected_contacts)
                return
            self.finished.emit(self.selected_contacts)
        except Exception as e:
            self.error_message.emit(e)
            self.finished.emit([])
        finally:
            if db_connection:
                db_connection.close()
                del db_connection
            QSqlDatabase.removeDatabase(self.connection_name)