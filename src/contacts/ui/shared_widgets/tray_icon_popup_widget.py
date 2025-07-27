from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout, QLabel


class TrayIconPopupWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("trayIconPopupWidget")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint, True)
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.popup_label = QLabel()
        self.popup_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.popup_label.setStyleSheet("font-size: 15pt;")
        main_layout.addWidget(self.popup_label)
        return main_layout

    def popup_set_text(self, title: str, message: str) -> None:
        self.popup_label.setText(f"{title}\n{message}")
