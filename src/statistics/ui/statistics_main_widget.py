from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QWidget, QLayout, QGridLayout, QTabWidget, QMainWindow

from src.statistics.controllers.statistics_controller import StatisticsController
from src.statistics.ui.statistics_widgets.mandatory_statistics_widget import MandatoryStatisticsWidget
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class StatisticsMainWidget(QWidget):
    def __init__(self, db_connection: QSqlDatabase, main_window: QMainWindow, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("statisticsMainWidget")
        self.db_connection = db_connection
        self.main_window = main_window
        self.statistics_controller = StatisticsController(self.db_connection, self, self.main_window)
        self.setLayout(self.create_gui())
        self.set_ui_text()
        self.statistics_controller.set_data()

    def create_gui(self) -> QLayout:
        main_layout = QGridLayout()
        self.statistics_tab_widget = QTabWidget()
        self.statistics_tab_widget.setObjectName("statisticsTabWidget")
        self.mandatory_statistics_widget = MandatoryStatisticsWidget(self.db_connection, self.main_window, self)
        self.mandatory_statistics_widget.setObjectName("mandatoryStatisticsWidget")
        self.test_tab = QWidget()
        self.test_tab.setObjectName("testTab")
        self.statistics_tab_widget.addTab(self.mandatory_statistics_widget, "")
        self.statistics_tab_widget.addTab(self.test_tab, "")
        main_layout.addWidget(self.statistics_tab_widget)
        return main_layout

    def set_ui_text(self) -> None:
        try:
            ui_text = LanguageProvider.get_ui_text(self.objectName())
            self.statistics_tab_widget.setTabText(0, ui_text.get("mandatoryStatisticsWidget", ""))
            self.statistics_tab_widget.setTabText(1, ui_text.get("testTab", ""))
        except Exception as e:
            ErrorHandler.exception_handler(e, self)