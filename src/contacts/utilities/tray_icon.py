import pathlib

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication, QWidget

from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("trayIcon")
        self.parent = parent
        self.setIcon(QIcon(str(pathlib.Path(__file__).parent.parent.parent.joinpath("icons", "mainWindow", "window_icon.png"))))
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
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)