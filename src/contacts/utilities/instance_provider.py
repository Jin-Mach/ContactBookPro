from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget

from src.utilities.error_handler import ErrorHandler


class InstanceProvider:

    @staticmethod
    def get_main_window_instance() -> QMainWindow | None:
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
    def get_contacts_controller_instance(controller: "ContactsController | None") -> "ContactsController | None":
        try:
            if controller is not None:
                return controller
            main_window = InstanceProvider.get_main_window_instance()
            if main_window is not None:
                contacts_toolbar = main_window.findChild(QWidget, "contactsToolbarWidget", Qt.FindChildOption.FindChildrenRecursively)
                if contacts_toolbar is not None:
                    controller = getattr(contacts_toolbar, "contacts_controller", None)
            return controller
        except Exception as e:
            ErrorHandler.exception_handler(e)
            return None