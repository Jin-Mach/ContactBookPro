import sys

from PyQt6.QtWidgets import QApplication

from src.main_window.main_window import MainWindow
from src.utilities.set_style import set_style


def create_application() -> None:
    application = QApplication(sys.argv)
    application.setStyle("fusion")
    set_style(application)
    window = MainWindow()
    window.show()
    sys.exit(application.exec())