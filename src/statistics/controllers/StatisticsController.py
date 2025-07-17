from typing import TYPE_CHECKING

from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMainWindow

from src.database.utilities.statistics_utilities.query_provider import QueryProvider
from src.statistics.threading.statistics_data_object import StatisticsDataObject
from src.utilities.error_handler import ErrorHandler

if TYPE_CHECKING:
    from src.statistics.ui.statistics_widgets.mandatory_statistics_widget import MandatoryStatisticsWidget


class StatisticsController:
    def __init__(self, db_connection: QSqlDatabase, mandatory_statistics_widget: "MandatoryStatisticsWidget",
                 main_window: QMainWindow) -> None:
        self.db_connection = db_connection
        self.mandatory_statistics_widget = mandatory_statistics_widget
        self.main_window = main_window

    def set_statistics_data(self) -> None:
        try:
            query_provider = QueryProvider()
            statistics_object = StatisticsDataObject(self.db_connection.databaseName(), query_provider)
            data = statistics_object.get_statistics_data()
            if not data:
                print("test")
                return
            self.mandatory_statistics_widget.set_data(data)
        except Exception as e:
            ErrorHandler.exception_handler(e, self.main_window)