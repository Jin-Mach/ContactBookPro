from PyQt6.QtWidgets import QWidget


class ManualMainWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("manualMainWidget")