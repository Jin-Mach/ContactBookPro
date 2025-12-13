from PyQt6.QtCore import QSettings, QSize, QPoint, QRect
from PyQt6.QtWidgets import QMainWindow, QApplication

from src.utilities.error_handler import ErrorHandler


class SettingsProvider:

    settings = QSettings("Jin-Mach", "ContactBookPro")

    @staticmethod
    def load_settings(main_window: QMainWindow, window_size: QSize) -> None:
        try:
            screen_geom = QApplication.primaryScreen().availableGeometry()
            store_size = SettingsProvider.settings.value("windowSize", window_size)
            if isinstance(store_size, (list, tuple)):
                store_size = QSize(int(store_size[0]), int(store_size[1]))
            store_position = SettingsProvider.settings.value("windowPosition", None)
            if store_position is None:
                store_position = QPoint(
                    (screen_geom.width() - store_size.width()) // 2,
                    (screen_geom.height() - store_size.height()) // 2
                )
            elif isinstance(store_position, (list, tuple)):
                store_position = QPoint(int(store_position[0]), int(store_position[1]))
            win_geom = QRect(store_position, store_size)
            if not screen_geom.intersects(win_geom):
                store_position = QPoint(
                    (screen_geom.width() - store_size.width()) // 2,
                    (screen_geom.height() - store_size.height()) // 2
                )
            main_window.resize(store_size)
            main_window.move(store_position)
            maximized = SettingsProvider.settings.value("windowMaximized", False, type=bool)
            if maximized:
                main_window.showMaximized()
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)

    @staticmethod
    def save_settings(main_window: QMainWindow) -> None:
        try:
            if main_window.isMaximized():
                SettingsProvider.settings.setValue("windowMaximized", True)
                SettingsProvider.settings.setValue("windowSize", main_window.normalGeometry().size())
                SettingsProvider.settings.setValue("windowPosition", main_window.normalGeometry().topLeft())
            else:
                SettingsProvider.settings.setValue("windowMaximized", False)
                SettingsProvider.settings.setValue("windowSize", main_window.size())
                SettingsProvider.settings.setValue("windowPosition", main_window.pos())
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)