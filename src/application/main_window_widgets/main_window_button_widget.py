import pathlib

from typing import Callable

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton, QSizePolicy

from src.utilities.error_handler import ErrorHandler


class MainWindowButtonWidget(QPushButton):
    def __init__(self, function: Callable[[], None], parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("mainWindowButton")
        self.setFixedHeight(50)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.setStyleSheet("""
            QPushButton {
                border: 1px solid;
                border-color: #448aff;
                text-align: left;
                padding-left: 0px;
                padding-right: 10px;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #448aff;
                color: white;
            }
            QPushButton:pressed {
                background-color: #80d0ff;
                color: white;
            }
        """)
        self.function = function
        self.clicked.connect(self.function)
        self.setIconSize(QSize(50, 50))

    def set_label_icon(self, object_name: str) -> None:
        try:
            icons_path = pathlib.Path(__file__).parents[3].joinpath("icons", "mainWindow")
            if icons_path.exists():
                icon_path = icons_path.joinpath(f"{object_name}_icon.png")
                if icon_path.exists():
                    icon = QIcon(str(icon_path))
                    self.setIcon(icon)
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_text(self, text: str) -> None:
        self.setText(text)
