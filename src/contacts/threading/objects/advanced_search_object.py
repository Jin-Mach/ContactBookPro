from typing import TYPE_CHECKING

from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

if TYPE_CHECKING:
    from src.database.utilities.contacts_utilities.query_provider import QueryProvider


# noinspection PyUnresolvedReferences
class AdvancedSearchObject(QObject):
    search_completed = pyqtSignal(list)
    error_message = pyqtSignal(str)
    finished = pyqtSignal(bool)
    def __init__(self, db_path: str, query_provider: "QueryProvider", filters: dict, parent=None) -> None:
        super().__init__()
        self.db_path = db_path
        self.query_provider = query_provider
        self.filters = filters
        self.parent = parent
        self.connection_name = f"advancedSearchThread{id(self)}"

    def run_advanced_search(self) -> None:
        db_connection = None
        try:
            id_list = []
            db_connection = QSqlDatabase.addDatabase("QSQLITE", self.connection_name)
            db_connection.setDatabaseName(self.db_path)
            if not db_connection.open():
                self.error_message.emit(db_connection.lastError().text())
                self.finished.emit(False)
                return
            sql_query, sql_values = self.query_provider.create_search_query(self.filters, self.parent)
            if not sql_query:
                self.finished.emit(False)
                return
            query = QSqlQuery(db_connection)
            query.prepare(sql_query)
            for value in sql_values:
                query.addBindValue(value)
            if not query.exec():
                self.error_message.emit(query.lastError().text())
                self.finished.emit(False)
                return
            while query.next():
                id_list.append(query.value(0))
            del query
            self.search_completed.emit(id_list)
            self.finished.emit(True)
        except Exception as e:
            self.error_message.emit(str(e))
            self.finished.emit(False)
        finally:
            if db_connection:
                db_connection.close()
                del db_connection
            QSqlDatabase.removeDatabase(self.connection_name)