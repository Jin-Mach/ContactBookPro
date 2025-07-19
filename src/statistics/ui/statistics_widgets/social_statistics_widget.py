from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout

from src.statistics.ui.statistics_widgets.chart_widgets.social_bar_char_widget import SocialBarCharWidget


class SocialStatisticsWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("socialStatisticsWidget")
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.social_bar = SocialBarCharWidget(self)
        main_layout.addWidget(self.social_bar)
        return main_layout