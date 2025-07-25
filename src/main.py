import sys

from PyQt6.QtWidgets import QApplication, QDialog

from src.application.main_window import MainWindow
from src.utilities.app_init import application_init
from src.utilities.dialogs_provider import DialogsProvider


def create_application() -> None:
    application = QApplication(sys.argv)
    if not application_init(application):
        result = DialogsProvider.show_init_error_dialog("Loading error",
                                                         "Critical error: Failed to load files from the GitHub repository."
                                                         "\nThe application will close now.")
        if result == QDialog.DialogCode.Accepted or result == QDialog.DialogCode.Rejected:
            sys.exit(1)
    window = MainWindow()
    application.main_window = window
    controller = window.contacts_main_widget.contacts_toolbar_widget.contacts_controller
    controller.update_locations()
    application.aboutToQuit.connect(controller.destroy_thread)
    window.show()
    sys.exit(application.exec())