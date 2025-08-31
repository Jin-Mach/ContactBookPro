from typing import TYPE_CHECKING

from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLayout, QTabWidget, QMainWindow, QVBoxLayout, QLabel

from src.statistics.controllers.statistics_controller import StatisticsController
from src.statistics.ui.statistics_widgets.basic_statistics_widget import BasicStatisticsWidget
from src.statistics.ui.statistics_widgets.completion_statistics_widget import CompletionStatisticsWidget
from src.statistics.ui.statistics_widgets.social_statistics_widget import SocialStatisticsWidget
from src.statistics.ui.statistics_widgets.work_statistics_widget import WorkStatisticsWidget
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider

if TYPE_CHECKING:
    from src.application.status_bar import StatusBar
    from src.database.models.mandatory_model import MandatoryModel


class StatisticsMainWidget(QWidget):
    def __init__(self, db_connection: QSqlDatabase, mandatory_model: "MandatoryModel", status_bar: "StatusBar",
                 main_window: QMainWindow, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("statisticsMainWidget")
        self.db_connection = db_connection
        self.mandatory_model = mandatory_model
        self.status_bar = status_bar
        self.main_window = main_window
        self.statistics_controller = StatisticsController(self.db_connection, self, self.main_window)
        self.setLayout(self.create_gui())
        self.set_ui_text()
        self.statistics_controller.set_data()

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.count_label = QLabel()
        self.count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.count_label.setStyleSheet("font-size: 20pt;")
        self.statistics_tab_widget = QTabWidget()
        self.statistics_tab_widget.setObjectName("statisticsTabWidget")
        self.basic_statistics_widget = BasicStatisticsWidget(self)
        self.basic_statistics_widget.setObjectName("mandatoryStatisticsWidget")
        self.work_statistics_widget = WorkStatisticsWidget(self)
        self.work_statistics_widget.setObjectName("workStatisticsWidget")
        self.social_statistics_widget = SocialStatisticsWidget(self)
        self.social_statistics_widget.setObjectName("socialStatisticsWidget")
        self.completion_statistics_widget = CompletionStatisticsWidget(self)
        self.completion_statistics_widget.setObjectName("completionStatisticsWidget")
        self.statistics_tab_widget.addTab(self.basic_statistics_widget, "")
        self.statistics_tab_widget.addTab(self.work_statistics_widget, "")
        self.statistics_tab_widget.addTab(self.social_statistics_widget, "")
        self.statistics_tab_widget.addTab(self.completion_statistics_widget, "")
        main_layout.addWidget(self.count_label)
        main_layout.addWidget(self.statistics_tab_widget)
        return main_layout

    def set_ui_text(self) -> None:
        try:
            self.ui_text = LanguageProvider.get_json_text("ui_text.json", self.objectName())
            if self.ui_text:
                self.statistics_tab_widget.setTabText(0, self.ui_text.get("mandatoryStatisticsWidget", ""))
                self.statistics_tab_widget.setTabText(1, self.ui_text.get("workStatisticsWidget", ""))
                self.statistics_tab_widget.setTabText(2, self.ui_text.get("socialStatisticsWidget", ""))
                self.statistics_tab_widget.setTabText(3, self.ui_text.get("completionStatisticsWidget"))
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_count_label_text(self) -> None:
        try:
            if self.ui_text:
                self.count_label.setText(f"{self.ui_text.get("totalCount", "")} {self.mandatory_model.total_rows}")
        except Exception as e:
            ErrorHandler.exception_handler(e, self)