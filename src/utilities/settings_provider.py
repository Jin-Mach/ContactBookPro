from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import QMainWindow

from src.utilities.error_handler import ErrorHandler


class SettingsProvider:

    settings = QSettings("Jin-Mach", "ContactBookPro")

    @staticmethod
    def load_settings(main_window: QMainWindow) -> None:
        try:
            geometry = SettingsProvider.settings.value("windowGeometry")
            if geometry is not None:
                main_window.restoreGeometry(geometry)
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)

    @staticmethod
    def save_settings(main_window: QMainWindow) -> None:
        try:
            SettingsProvider.settings.setValue(
                "windowGeometry",
                main_window.saveGeometry()
            )
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)