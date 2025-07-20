from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout

from src.statistics.ui.statistics_widgets.chart_widgets.completion_bar_chart_widget import CompletionBarChartWidget


class CompletionStatisticsWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("completionStatisticsWidget")
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.detail_bar = CompletionBarChartWidget(self)
        main_layout.addWidget(self.detail_bar)
        return main_layout