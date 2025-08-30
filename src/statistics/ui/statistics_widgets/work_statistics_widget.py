from PyQt6.QtWidgets import QWidget, QLayout, QGridLayout

from src.statistics.ui.statistics_widgets.chart_widgets.city_bar_chart_widget import CityBarChartWidget
from src.statistics.ui.statistics_widgets.chart_widgets.work_pie_chart_widget import WorkPieChartWidget


class WorkStatisticsWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("workStatisticsWidget")
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QGridLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.email_pie = WorkPieChartWidget("email", self)
        self.phone_pie = WorkPieChartWidget("phone", self)
        self.city_bar = CityBarChartWidget("work", self)
        main_layout.addWidget(self.email_pie, 0, 0)
        main_layout.addWidget(self.phone_pie, 0, 1)
        main_layout.addWidget(self.city_bar, 1, 0, 1, 3)
        return main_layout