from typing import TYPE_CHECKING, Any

from PyQt6.QtCore import QThread
from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMainWindow

from src.database.utilities.statistics_utilities.query_provider import QueryProvider
from src.statistics.threading.statistics_data_object import StatisticsDataObject
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider

if TYPE_CHECKING:
    from src.statistics.ui.statistics_main_widget import StatisticsMainWidget


# noinspection PyUnresolvedReferences,PyArgumentList
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

    def set_statistics_data(self, data: dict[str, dict[str, Any]]) -> None:
        try:
            ui_text = LanguageProvider.get_ui_text("statisticsController")
            handlers = {
                "basic": self.set_basic,
                "work": self.set_work,
                "social": self.set_social,
                "completion": self.set_completion
            }
            for key, handler in handlers.items():
                if key in data:
                    handler(data[key])
            self.statistics_main_widget.status_bar.show_status_bar_message(ui_text.get("statisticsUpdate", ""))
        except Exception as e:
            ErrorHandler.exception_handler(e, self.main_window)

    def set_basic(self, basic_data: dict[str, Any]) -> None:
        try:
            self.statistics_main_widget.basic_statistics_widget.gender_pie.draw_pie(basic_data.get("gender", ""))
            self.statistics_main_widget.basic_statistics_widget.relationship_bar.draw_bar(basic_data.get("relationship", ""))
            self.statistics_main_widget.basic_statistics_widget.city_bar.draw_bar(basic_data.get("personal_city", ""))
        except Exception as e:
            ErrorHandler.exception_handler(e, self.main_window)

    def set_work(self, basic_data: dict[str, Any]) -> None:
        try:
            self.statistics_main_widget.work_statistics_widget.email_pie.draw_pie(basic_data.get("work_email", ""))
            self.statistics_main_widget.work_statistics_widget.phone_pie.draw_pie(basic_data.get("work_phone_number", ""))
            self.statistics_main_widget.work_statistics_widget.city_bar.draw_bar(basic_data.get("work_city", ""))
        except Exception as e:
            ErrorHandler.exception_handler(e, self.main_window)

    def set_social(self, basic_data: dict) -> None:
        try:
            self.statistics_main_widget.social_statistics_widget.social_bar.draw_bar(basic_data.get("social_all", ""))
        except Exception as e:
            ErrorHandler.exception_handler(e, self.main_window)

    def set_completion(self, basic_data: dict) -> None:
        try:
            self.statistics_main_widget.completion_statistics_widget.total_bar.draw_bar(basic_data)
            self.statistics_main_widget.completion_statistics_widget.detail_bar.draw_bar(basic_data)
        except Exception as e:
            ErrorHandler.exception_handler(e, self.main_window)