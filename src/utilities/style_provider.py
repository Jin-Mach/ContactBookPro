from PyQt6.QtWidgets import QApplication
from qt_material import apply_stylesheet


def set_application_style(application: QApplication) -> None:
    apply_stylesheet(application, theme="dark_blue.xml")