import pathlib

from typing import Callable

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QSizePolicy

from src.utilities.error_handler import ErrorHandler


# noinspection PyUnresolvedReferences
class MainWindowButtonWidget(QFrame):
    def __init__(self, function: Callable[[], None], parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("mainWindowButtonWidget")
        self.setMinimumSize(QSize(200, 50))
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.function = function
        self.setLayout(self.create_gui())
        self.setStyleSheet(self.get_stylesheet())

    def create_gui(self) -> QLayout:
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.icon_label = QLabel()
        self.icon_label.setFixedWidth(50)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button = QPushButton()
        self.button.setObjectName("button")
        self.button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.button.setStyleSheet(self.get_stylesheet())
        self.button.setFlat(True)
        self.button.clicked.connect(self.function)
        main_layout.addWidget(self.icon_label)
        main_layout.addWidget(self.button, 1)
        return main_layout

    def set_label_icon(self, object_name: str) -> None:
        try:
            icons_path = pathlib.Path(__file__).parents[3].joinpath("icons", "mainWindow")
            if icons_path.exists():
                pixmap = QPixmap(str(icons_path.joinpath(f"{object_name}_icon.png")))
                self.icon_label.setPixmap(pixmap.scaled(QSize(40, 40), Qt.AspectRatioMode.KeepAspectRatio,
                                                             Qt.TransformationMode.SmoothTransformation))
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

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
