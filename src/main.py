import sys

from PyQt6.QtWidgets import QApplication

from src.main_window.main_window import MainWindow
from src.utilities.style_manager import Stylemanager


def create_application() -> None:
    application = QApplication(sys.argv)
    application.setStyle("fusion")
    Stylemanager.set_style(application)
    window = MainWindow()
    window.show()
    sys.exit(application.exec())