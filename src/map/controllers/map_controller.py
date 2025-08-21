from typing import TYPE_CHECKING

from PyQt6.QtCore import QThread
from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMainWindow

from src.database.utilities.map_utilities.query_provider import QueryProvider
from src.map.threading.generate_map_object import GenerateMapObject
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider

if TYPE_CHECKING:
    from src.map.ui.map_main_widget import MapMainWidget


# noinspection PyUnresolvedReferences
class MapController:
    def __init__(self, db_connection: QSqlDatabase, map_main_widget: "MapMainWidget", main_window: QMainWindow) -> None:
        self.class_name = "mapController"
        self.db_connection = db_connection
        self.map_main_widget = map_main_widget
        self.main_window = main_window

    def create_map(self) -> None:
        try:
            self.query_provider = QueryProvider()
            self.map_object = GenerateMapObject(self.db_connection.databaseName(), self.query_provider)
            self.thread = QThread()
            self.map_object.moveToThread(self.thread)
            self.thread.started.connect(self.map_object.generate_map)
            self.map_object.map_ready.connect(self.set_map)
            self.map_object.finished.connect(self.thread.quit)
            self.map_object.finished.connect(self.map_object.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.thread.start()
        except Exception as e:
            ErrorHandler.exception_handler(e, self.main_window)

    def set_map(self, html: str, count: int, connection: bool) -> None:
        try:
            ui_text = LanguageProvider.get_ui_text(self.class_name)
            self.map_main_widget.load_map(html, count, connection)
            self.map_main_widget.status_bar.show_status_bar_message(ui_text.get("mapUpdate", ""))
        except Exception as e:
            ErrorHandler.exception_handler(e, self.main_window)