from typing import TYPE_CHECKING

from PyQt6.QtCore import QThread
from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMainWindow

from src.database.utilities.statistics_utilities.query_provider import QueryProvider
from src.statistics.threading.statistics_data_object import StatisticsDataObject
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider

if TYPE_CHECKING:
    from src.statistics.ui.statistics_main_widget import StatisticsMainWidget


# noinspection PyUnresolvedReferences
class StatisticsController:
    def __init__(self, db_connection: QSqlDatabase, statistics_main_widget: "StatisticsMainWidget",
                 main_window: QMainWindow) -> None:
        self.class_name = "statisticsController"
        self.db_connection = db_connection
        self.statistics_main_widget = statistics_main_widget
        self.main_window = main_window

    def set_data(self) -> None:
        try:
            self.query_provider = QueryProvider()
            self.statistics_object = StatisticsDataObject(self.db_connection.databaseName(), self.query_provider)
            self.thread = QThread()
            self.statistics_object.moveToThread(self.thread)
            self.thread.started.connect(self.statistics_object.get_statistics_data)
            self.statistics_object.data_ready.connect(self.set_statistics_data)
            self.statistics_object.finished.connect(self.thread.quit)
            self.statistics_object.finished.connect(self.statistics_object.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.thread.start()
        except Exception as e:
            ErrorHandler.exception_handler(e, self.main_window)

    def set_statistics_data(self, data: dict) -> None:
        try:
            ui_text = LanguageProvider.get_ui_text("statisticsController")
            self.statistics_main_widget.mandatory_statistics_widget.gender_pie.draw_pie(data.get("gender", ""))
            self.statistics_main_widget.mandatory_statistics_widget.relationship_bar.draw_bar(data.get("relationship", ""))
            self.statistics_main_widget.status_bar.show_statusbar_message(ui_text.get("statisticsUpdate", ""))
        except Exception as e:
            ErrorHandler.exception_handler(e, self.main_window)