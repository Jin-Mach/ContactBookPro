from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLayout, QGridLayout, QLabel

from src.statistics.ui.statistics_widgets.chart_widgets.relationship_bar_chart_widget import RelationshipBarChartWidget
from src.statistics.ui.statistics_widgets.chart_widgets.gender_pie_chart_widget import GenderPieChartWidget
from src.statistics.ui.statistics_widgets.chart_widgets.city_bar_chart_widget import CityBarChartWidget

if TYPE_CHECKING:
    from src.statistics.ui.statistics_main_widget import StatisticsMainWidget


class BasicStatisticsWidget(QWidget):
    def __init__(self, statistics_main_widget: "StatisticsMainWidget",
                 parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("basicStatisticsWidget")
        self.statistics_main_widget = statistics_main_widget
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QGridLayout()
        self.count_label = QLabel()
        self.count_label.setStyleSheet("font-size: 25pt")
        self.count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gender_pie = GenderPieChartWidget(self.statistics_main_widget.set_count_label_text, self)
        self.relationship_bar = RelationshipBarChartWidget(self)
        self.city_bar = CityBarChartWidget(self)
        main_layout.addWidget(self.count_label, 0, 0, 1, 2)
        main_layout.addWidget(self.gender_pie, 1, 0)
        main_layout.addWidget(self.relationship_bar, 1, 1)
        main_layout.addWidget(self.city_bar, 2, 0, 1, 2)
        return main_layout