from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QWidget, QLayout, QGridLayout, QMainWindow

from src.statistics.controllers.StatisticsController import StatisticsController


class MandatoryStatisticsWidget(QWidget):
    def __init__(self, db_connection: QSqlDatabase, main_window: QMainWindow, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("mandatoryStatisticsWidget")
        self.db_connection = db_connection
        self.main_window = main_window
        self.setLayout(self.create_gui())
        self.statistics_controller = StatisticsController(self.db_connection, self, self.main_window)
        self.statistics_controller.set_statistics_data()

    def create_gui(self) -> QLayout:
        main_layout = QGridLayout()
        return main_layout

    def set_data(self, data) -> None:
        print(data)