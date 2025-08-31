import pathlib

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QLayout, QLabel, QGridLayout, QVBoxLayout, QFrame

from src.utilities.error_handler import ErrorHandler


class TrayIconPopupWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("trayIconPopupWidget")
        self.setMinimumSize(200, 50)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint, True)
        self.setLayout(self.create_gui())
        self.set_icon()
        self.set_styles()

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.frame = QFrame()
        grid_layout = QGridLayout(self.frame)
        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label = QLabel()
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(self.icon_label, 0, 0)
        grid_layout.addWidget(self.title_label, 0, 1)
        grid_layout.addWidget(self.message_label, 1, 1)
        main_layout.addWidget(self.frame)
        return main_layout

    def set_icon(self) -> None:
        try:
            icon_path = pathlib.Path(__file__).parents[4].joinpath("icons", "mainWindow")
            if icon_path.exists():
                pixmap = QPixmap(str(icon_path.joinpath("mainWindowLogo.png")))
                self.icon_label.setPixmap(pixmap.scaled(QSize(25, 25), Qt.AspectRatioMode.KeepAspectRatio,
                                                         Qt.TransformationMode.SmoothTransformation))
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_styles(self) -> None:
        self.frame.setStyleSheet("""border-top: 2px solid #2196F3;
                                    border-left: 2px solid #2196F3;
                                    border-right: 2px solid #2196F3;
                                    border-bottom: 2px solid #2196F3;
                                    """)
        self.icon_label.setStyleSheet("border: none;")
        self.title_label.setStyleSheet("font-size: 15pt; border: none;")
        self.message_label.setStyleSheet("font-size: 12pt; border: none;")

    def popup_set_text(self, title: str, message: str) -> None:
        self.title_label.setText(title)
        self.message_label.setText(message)
        self.setMinimumSize(0, 0)