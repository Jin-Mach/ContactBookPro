from typing import Optional, TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget

from src.utilities.error_handler import ErrorHandler

if TYPE_CHECKING:
    from src.controlers.contacts_controller import ContactsController


class InstanceProvider:

    @staticmethod
    def get_main_window_instance() -> Optional[QMainWindow]:
        try:
            application = QApplication.instance()
            if application is None:
                return None
            main_window = getattr(application, "main_window", None)
            if isinstance(main_window, QMainWindow):
                return main_window
            return None
        except Exception as e:
            ErrorHandler.exception_handler(e)
            return None

    @staticmethod
    def get_contacts_controler_instance(controler: "Optional[ContactsController]") -> "Optional[ContactsController]":
        try:
            if controler is not None:
                return controler
            main_window = InstanceProvider.get_main_window_instance()
            if main_window is not None:
                contacts_toolbar = main_window.findChild(QWidget, "contactsToolbarWidget", Qt.FindChildOption.FindChildrenRecursively)
                if contacts_toolbar is not None:
                    controler = getattr(contacts_toolbar, "contacts_controler", None)
            return controler
        except Exception as e:
            ErrorHandler.exception_handler(e)
            return None