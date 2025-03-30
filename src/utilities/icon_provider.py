import pathlib

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton, QWidget, QToolButton

from src.utilities.error_handler import ErrorHandler


class IconProvider:
    icons_path = pathlib.Path(__file__).parent.parent.joinpath("icons")

    @staticmethod
    def set_window_icon(widget: QWidget, widget_name: str, parent=None) -> None:
        icon_icon_file = IconProvider.icons_path.joinpath(f"{widget_name}", "window_icon.png")
        try:
            if icon_icon_file.exists():
                widget.setWindowIcon(QIcon(str(icon_icon_file)))
        except Exception as e:
            ErrorHandler.exception_handler(e, parent)

    @staticmethod
    def set_buttons_icon(widget_name: str, widgets: list[QWidget], button_size: QSize | None, parent=None) -> None:
        icon_path = IconProvider.icons_path.joinpath(widget_name)
        try:
            if icon_path.exists():
                for widget in widgets:
                    icon_file = icon_path.joinpath(f"{widget.objectName()}_icon.png")
                    if isinstance(widget, QPushButton):
                        if icon_file.exists():
                            widget.setIcon(QIcon(str(icon_file)))
                            widget.setIconSize(button_size)
                    elif isinstance(widget, QToolButton):
                        if icon_file.exists():
                            widget.setIcon(QIcon(str(icon_file)))
        except Exception as e:
            ErrorHandler.exception_handler(e, parent)