import pathlib
from typing import Optional

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

    def create_context_menu(self) -> Optional[QMenu]:
        ui_text = LanguageProvider.get_ui_text(self.objectName())
        try:
            menu = QMenu()
            self.new_contact = menu.addAction(ui_text["addContact"])
            self.close_application = menu.addAction(ui_text["closeApplication"])
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
            self.showMessage(title, ui_text[message], QSystemTrayIcon.MessageIcon.Information, 5000)
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)