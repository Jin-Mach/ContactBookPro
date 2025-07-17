from PyQt6.QtWidgets import QWidget, QLayout, QGridLayout


class StatisticsMainWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("statisticsMainWidget")
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QGridLayout()
        return main_layout