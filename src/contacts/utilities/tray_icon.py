import pathlib

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication, QWidget

from src.application.status_bar import StatusBar
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class TrayIcon(QSystemTrayIcon):
    icon_path = pathlib.Path(__file__).parents[3].joinpath("icons", "mainWindow", "window_icon.png")

    def __init__(self, status_bar: StatusBar, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("trayIcon")
        self.status_bar = status_bar
        self.parent = parent
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
                self.showMessage(title, ui_text.get(message, ""), QSystemTrayIcon.MessageIcon.Information, 5000)
                self.status_bar.show_statusbar_message(ui_text.get(message, ""))
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)