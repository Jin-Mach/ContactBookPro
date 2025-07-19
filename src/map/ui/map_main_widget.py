from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout, QMainWindow, QLabel

from src.map.controllers.map_controller import MapController

if TYPE_CHECKING:
    from src.application.status_bar import StatusBar


class MapMainWidget(QWidget):
    def __init__(self, db_connection: QSqlDatabase, status_bar: "StatusBar", main_window: QMainWindow,
                 parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("mapMainWidget")
        self.db_connection = db_connection
        self.status_bar = status_bar
        self.main_window = main_window
        self.map_controller = MapController(self.db_connection, self, self.main_window)
        self.setLayout(self.create_gui())
        self.map_controller.create_map()

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.no_data_label = QLabel("text...")
        self.no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_data_label.setStyleSheet("font-size: 25pt")
        self.no_data_label.hide()
        self.web_view = QWebEngineView()
        main_layout.addWidget(self.no_data_label)
        main_layout.addWidget(self.web_view)
        return main_layout

    def show_map(self, html_map: str) -> None:
        html_map = ""
        if not html_map:
            self.web_view.hide()
            self.no_data_label.show()
        else:
            self.web_view.setHtml(html_map)
            self.web_view.show()