from PyQt6.QtCore import QSettings, QSize, QPoint
from PyQt6.QtWidgets import QMainWindow, QApplication

from src.utilities.error_handler import ErrorHandler


class SettingsProvider:

    settings = QSettings("Jin-Mach", "ContactBookPro")

    @staticmethod
    def load_settings(main_window: QMainWindow, window_size: QSize) -> None:
        try:
            screen_size = QApplication.primaryScreen().size()
            store_size = SettingsProvider.settings.value("windowSize", None)
            store_position = SettingsProvider.settings.value("windowPosition",
                                                             QPoint(screen_size.width() // 2, screen_size.height() // 2))
            if store_size is None:
                store_size = window_size
            if store_size.width() < screen_size.width() and store_size.height() < screen_size.height():
                main_window.resize(store_size)
                main_window.move(store_position)
            else:
                main_window.showMaximized()
                main_window.move(store_position)
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)

    @staticmethod
    def save_settings(main_window: QMainWindow) -> None:
        try:
            SettingsProvider.settings.setValue("windowSize", main_window.size())
            SettingsProvider.settings.setValue("windowPosition", main_window.pos())
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)