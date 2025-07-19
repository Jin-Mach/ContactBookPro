from typing import TYPE_CHECKING

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtSql import QSqlDatabase

from src.map.utilitites.map_provider import create_map

if TYPE_CHECKING:
    from src.database.utilities.map_utilities.query_provider import QueryProvider


# noinspection PyBroadException,PyUnresolvedReferences
class GenerateMapObject(QObject):
    map_ready = pyqtSignal(str)
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
            if not db_connection.open():
                self.map_ready.emit(contacts_map)
                self.finished.emit()
                return
            contacts_data = self.query_provider.get_maps_contacts(db_connection)
            if not contacts_data:
                self.map_ready.emit(contacts_map)
                self.finished.emit()
                return
            contacts_map = create_map(contacts_data)
            self.map_ready.emit(contacts_map)
            self.finished.emit()
        except Exception:
            self.map_ready.emit(contacts_map)
            self.finished.emit()
        finally:
            if db_connection:
                db_connection.close()
                del db_connection
            QSqlDatabase.removeDatabase(self.connection_name)