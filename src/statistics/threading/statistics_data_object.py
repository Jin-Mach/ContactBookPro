from typing import TYPE_CHECKING

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtSql import QSqlDatabase

if TYPE_CHECKING:
    from src.database.utilities.statistics_utilities.query_provider import QueryProvider


# noinspection PyUnresolvedReferences,PyBroadException
class StatisticsDataObject(QObject):
    data_ready = pyqtSignal(dict)
    finished = pyqtSignal()
    def __init__(self, db_path: str, query_provider: "QueryProvider") ->  None:
        super().__init__()
        self.setObjectName("statisticsDataObject")
        self.db_path = db_path
        self.query_provider = query_provider
        self.connection_name = f"statisticsDataThread{id(self)}"

    def get_statistics_data(self):
        db_connection = None
        results = {
            "basic": {},
            "work": {},
            "social": {}
        }
        try:
            db_connection = QSqlDatabase.addDatabase("QSQLITE", self.connection_name)
            db_connection.setDatabaseName(self.db_path)
            if not db_connection.open():
                self.data_ready.emit(results)
                self.finished.emit()
                return
            results["basic"]["gender"] = self.query_provider.get_basic_statistics_data(db_connection, "gender")
            results["basic"]["relationship"] = self.query_provider.get_basic_statistics_data(db_connection, "relationship")
            results["basic"]["personal_city"] = self.query_provider.get_basic_statistics_data(db_connection, "personal_city")
            results["basic"]["personal_country"] = self.query_provider.get_basic_statistics_data(db_connection, "personal_country")
            results["work"]["work_email"] = self.query_provider.get_work_statistics_data(db_connection, "work_email")
            results["work"]["work_phone_number"] = self.query_provider.get_work_statistics_data(db_connection, "work_phone_number")
            results["work"]["work_city"] = self.query_provider.get_work_statistics_data(db_connection, "work_city")
            results["social"]["social_all"] = self.query_provider.get_social_statistics_data(db_connection)
            self.data_ready.emit(results)
            self.finished.emit()
        except Exception:
            self.data_ready.emit(results)
            self.finished.emit()
        finally:
            if db_connection:
                db_connection.close()
                del db_connection
            QSqlDatabase.removeDatabase(self.connection_name)