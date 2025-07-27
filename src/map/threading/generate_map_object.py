from typing import TYPE_CHECKING

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtSql import QSqlDatabase

from src.utilities.application_support_provider import ApplicationSupportProvider
from src.map.utilities.map_provider import create_map

if TYPE_CHECKING:
    from src.database.utilities.map_utilities.query_provider import QueryProvider


# noinspection PyBroadException,PyUnresolvedReferences
class GenerateMapObject(QObject):
    map_ready = pyqtSignal(str, int, bool)
    finished = pyqtSignal()
    def __init__(self, db_path: str, query_provider: "QueryProvider") -> None:
        super().__init__()
        self.setObjectName("generateMapObject")
        self.db_path = db_path
        self.query_provider = query_provider
        self.connection_name = f"generateMapThread{id(self)}"

    def generate_map(self) -> None:
        db_connection = None
        contacts_map = ""
        try:
            db_connection = QSqlDatabase.addDatabase("QSQLITE", self.connection_name)
            db_connection.setDatabaseName(self.db_path)
            is_connect = ApplicationSupportProvider.connection_result()
            if not is_connect:
                self.map_ready.emit(contacts_map, 0, is_connect)
                self.finished.emit()
                return
            if not db_connection.open():
                self.map_ready.emit(contacts_map, 0, is_connect)
                self.finished.emit()
                return
            contacts_data = self.query_provider.get_maps_contacts(db_connection)
            if not contacts_data:
                self.map_ready.emit(contacts_map, 0, is_connect)
                self.finished.emit()
                return
            contacts_map = create_map(contacts_data)
            self.map_ready.emit(contacts_map, len(contacts_data), is_connect)
            self.finished.emit()
        except Exception:
            self.map_ready.emit(contacts_map, 0, False)
            self.finished.emit()
        finally:
            if db_connection:
                db_connection.close()
                del db_connection
            QSqlDatabase.removeDatabase(self.connection_name)