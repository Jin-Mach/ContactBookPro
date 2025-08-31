import pathlib

from typing import TYPE_CHECKING

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication, QWidget

from src.contacts.ui.shared_widgets.tray_icon_popup_widget import TrayIconPopupWidget
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider

if TYPE_CHECKING:
    from src.application.main_window import MainWindow
    from src.application.status_bar import StatusBar


# noinspection PyUnresolvedReferences
class TrayIcon(QSystemTrayIcon):
    icon_path = pathlib.Path(__file__).parents[3].joinpath("icons", "mainWindow", "mainWindowLogo.png")

    def __init__(self, status_bar: "StatusBar", parent: "MainWindow") -> None:
        super().__init__(parent)
        self.setObjectName("trayIcon")
        self.status_bar = status_bar
        self.parent = parent
        self.popup_widget = TrayIconPopupWidget(self.parent)
        if self.icon_path.exists():
            self.setIcon(QIcon(str(self.icon_path)))
        menu = self.create_context_menu()
        if menu:
            self.setContextMenu(menu)
            self.create_connection()

    def create_context_menu(self) -> QMenu | None:
        try:
            ui_text = LanguageProvider.get_ui_text(self.objectName())
            menu = QMenu()
            if ui_text:
                self.new_contact = menu.addAction(ui_text.get("addContact", ""))
                self.close_application = menu.addAction(ui_text.get("closeApplication", ""))
            return menu
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)
            return None

    def create_connection(self) -> None:
        try:
            toolbar = self.parent.findChild(QWidget, "contactsToolbarWidget")
            self.new_contact.triggered.connect(toolbar.add_new_contact)
            self.close_application.triggered.connect(QApplication.quit)
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def show_notification(self, title: str, message: str) -> None:
        try:
            ui_text = LanguageProvider.get_ui_text("trayIcon")
            if ui_text:
                self.popup_widget.popup_set_text(title, ui_text.get(message, ""))
                self.popup_widget.show()
                self.finalize_popup(self.popup_widget)
                self.status_bar.show_status_bar_message(ui_text.get(message, ""))
                QTimer.singleShot(3000, self.popup_widget.close)
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    @staticmethod
    def finalize_popup(popup_widget: TrayIconPopupWidget) -> None:
        popup_widget.adjustSize()
        parent = popup_widget.parent()
        if parent is not None:
            geometry = parent.geometry()
            x = geometry.x() + geometry.width() - popup_widget.width() - 10
            y = geometry.y() + geometry.height() - popup_widget.height() - 10
            popup_widget.move(x, y)