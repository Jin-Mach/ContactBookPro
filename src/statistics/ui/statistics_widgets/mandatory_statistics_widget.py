from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QWidget, QLayout, QGridLayout, QMainWindow

from src.statistics.ui.statistics_widgets.pie_chart_widget import PieChartWidget


class MandatoryStatisticsWidget(QWidget):
    def __init__(self, db_connection: QSqlDatabase, main_window: QMainWindow, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("mandatoryStatisticsWidget")
        self.db_connection = db_connection
        self.main_window = main_window
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QGridLayout()
        self.gender_pie = PieChartWidget(self)
        main_layout.addWidget(self.gender_pie, 0, 0)
        return main_layout