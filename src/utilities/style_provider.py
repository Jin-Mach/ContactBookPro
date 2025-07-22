from qt_material import apply_stylesheet

from PyQt6.QtWidgets import QApplication


def set_application_style(application: QApplication) -> None:
    apply_stylesheet(application, "dark_blue.xml")