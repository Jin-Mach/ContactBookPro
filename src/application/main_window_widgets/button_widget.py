import pathlib
from typing import Callable

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import QLayout, QHBoxLayout, QLabel, QPushButton, QFrame


# noinspection PyUnresolvedReferences
class MainWindowButtonWidget(QFrame):
    def __init__(self, function: Callable[[], None], parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("mainWindowButtonWidget")
        self.setFixedSize(QSize(200, 50))
        self.function = function
        self.setLayout(self.create_gui())
        self.setStyleSheet(self.get_stylesheet())

    def create_gui(self) -> QLayout:
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button = QPushButton()
        self.button.setObjectName("button")
        self.button.setFont(QFont("Arial", 15))
        self.button.setFlat(True)
        self.button.clicked.connect(self.function)
        main_layout.addWidget(self.icon_label)
        main_layout.addWidget(self.button)
        return main_layout

    def set_label_icon(self, object_name: str) -> None:
        icons_path = pathlib.Path(__file__).parents[3].joinpath("icons", "mainWindow")
        pixmap = QPixmap(str(icons_path.joinpath(f"{object_name}_icon.png")))
        self.icon_label.setPixmap(pixmap.scaled(QSize(40, 40), Qt.AspectRatioMode.KeepAspectRatio,
                                                     Qt.TransformationMode.SmoothTransformation))

    def set_text(self, text: str) -> None:
        self.button.setText(text)

    @staticmethod
    def get_stylesheet() -> str:
        return """QFrame#mainWindowButtonWidget {
        border: 1px solid #448aff;
        border-radius: 6px;
        background-color: transparent;
    }
    QPushButton#button {
        border: none;
        font-size: 15pt;
    }
    """
