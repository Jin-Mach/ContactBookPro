import pathlib

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QPushButton, QWidget, QMenu

from src.utilities.error_handler import ErrorHandler


class IconProvider:
    icons_path = pathlib.Path(__file__).parents[2].joinpath("icons")

    @staticmethod
    def set_window_icon(widget: QWidget, folder_name: str) -> None:
        try:
            icon_icon_file = IconProvider.icons_path.joinpath(f"{folder_name}", "mainWindowLogo.png")
            if icon_icon_file.exists():
                widget.setWindowIcon(QIcon(str(icon_icon_file)))
        except Exception as e:
            ErrorHandler.exception_handler(e, widget)

    @staticmethod
    def set_buttons_icon(widget_name: str, widgets: list[QWidget], button_size: QSize | None, parent=None) -> None:
        try:
            icon_path = IconProvider.icons_path.joinpath(widget_name)
            if icon_path.exists():
                for widget in widgets:
                    icon_file = icon_path.joinpath(f"{widget.objectName()}_icon.png")
                    if isinstance(widget, QPushButton):
                        if icon_file.exists():
                            widget.setIcon(QIcon(str(icon_file)))
                            widget.setIconSize(button_size)
                    elif isinstance(widget, QMenu):
                        if icon_file.exists():
                            widget.setIcon(QIcon(str(icon_file)))
                    elif isinstance(widget, QAction):
                        if icon_file.exists():
                            widget.setIcon(QIcon(str(icon_file)))
                            widget.setIconVisibleInMenu(True)
        except Exception as e:
            ErrorHandler.exception_handler(e, parent)