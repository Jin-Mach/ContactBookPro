from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout, QLabel

from src.statistics.ui.statistics_widgets.chart_widgets.completion_bar_chart_widget import CompletionBarChartWidget


class CompletionStatisticsWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("completionStatisticsWidget")
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.header_widget = QLabel()
        self.total_bar = CompletionBarChartWidget(True, self)
        self.total_bar.setFixedHeight(120)
        self.detail_bar = CompletionBarChartWidget(False, self)
        main_layout.addWidget(self.total_bar)
        main_layout.addWidget(self.detail_bar)
        return main_layout