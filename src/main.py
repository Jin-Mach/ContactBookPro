import sys

from PyQt6.QtWidgets import QApplication

from src.main_window.main_window import MainWindow
from src.utilities.style_provider import StyleProvider


def create_application() -> None:
    application = QApplication(sys.argv)
    application.setStyle("fusion")
    StyleProvider.set_style(application)
    window = MainWindow()
    window.show()
    sys.exit(application.exec())