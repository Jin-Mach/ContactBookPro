from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout, QMainWindow, QLabel

from src.map.controllers.map_controller import MapController
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider

if TYPE_CHECKING:
    from src.database.models.mandatory_model import MandatoryModel
    from src.application.status_bar import StatusBar


class MapMainWidget(QWidget):
    def __init__(self, db_connection: QSqlDatabase, mandatory_model: "MandatoryModel", status_bar: "StatusBar",
                 main_window: QMainWindow,
                 parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("mapMainWidget")
        self.db_connection = db_connection
        self.mandatory_model = mandatory_model
        self.status_bar = status_bar
        self.main_window = main_window
        self.map_controller = MapController(self.db_connection, self, self.main_window)
        self.setLayout(self.create_gui())
        self.map_controller.create_map()

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.loading_map_label = QLabel()
        self.loading_map_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_map_label.setStyleSheet("font-size: 12pt")
        self.loading_map_label.hide()
        self.contacts_count_label = QLabel()
        self.contacts_count_label.setFixedHeight(20)
        self.contacts_count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.contacts_count_label.setStyleSheet("font-size: 12pt")
        self.contacts_count_label.hide()
        self.web_view = QWebEngineView()
        self.web_view.hide()
        self.web_view.loadFinished.connect(self.show_map)
        main_layout.addWidget(self.loading_map_label)
        main_layout.addWidget(self.contacts_count_label)
        main_layout.addWidget(self.web_view)
        return main_layout

    def load_map(self, html_map: str, count: int, connection: bool) -> None:
        try:
            ui_text = LanguageProvider.get_json_text("ui_text.json", self.objectName())
            self.has_connection = connection
            if not self.has_connection or html_map.strip() == "":
                self.loading_map_label.setText(ui_text.get("noConnection", ""))
                self.loading_map_label.show()
                self.contacts_count_label.hide()
                self.web_view.hide()
            else:
                self.loading_map_label.setText(f"{ui_text.get("loadingMap", "")}")
                self.loading_map_label.show()
                self.contacts_count_label.setText(f"{ui_text.get("showCount", "")} {count} "
                                                  f"({ui_text.get("totalCount", "")} {self.mandatory_model.total_rows})")
                self.contacts_count_label.hide()
                self.web_view.hide()
                self.web_view.setHtml(html_map)
        except Exception as e:
            ErrorHandler.exception_handler(e, self.main_window)

    def show_map(self, state: bool) -> None:
        try:
            if state:
                self.loading_map_label.hide()
                self.contacts_count_label.show()
                self.web_view.show()
            else:
                if self.has_connection:
                    ui_text = LanguageProvider.get_json_text("ui_text.json", self.objectName())
                    self.contacts_count_label.hide()
                    self.web_view.hide()
                    self.loading_map_label.setText(f"{ui_text.get("loadingError", "")}")
                    self.loading_map_label.show()
        except Exception as e:
            ErrorHandler.exception_handler(e, self.main_window)