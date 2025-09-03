import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QDialog

from src.application.main_window import MainWindow
from src.utilities.app_init import application_init, files_init
from src.utilities.application_support_provider import ApplicationSupportProvider
from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.splash_screen import SplashScreen


def create_application() -> None:
    debug = True
    application_support_provider = ApplicationSupportProvider()
    application_support_provider.hide_mac_traceback(debug)
    application = QApplication(sys.argv)
    if not files_init(application_support_provider):
        result = DialogsProvider.show_init_error_dialog("Loading error",
                                                         "Failed to load files from the GitHub repository."
                                                         "\nCheck your internet connection."
                                                         "\nThe application will close now.")
        if result == QDialog.DialogCode.Accepted or result == QDialog.DialogCode.Rejected:
            sys.exit(1)
    splash_screen = SplashScreen()
    splash_screen.show()
    QApplication.processEvents()
    if not application_init(application, application_support_provider):
        result = DialogsProvider.show_init_error_dialog("Loading error",
                                                         "Failed during application setup."
                                                         "\nThe application will close now.")
        if result == QDialog.DialogCode.Accepted or result == QDialog.DialogCode.Rejected:
            sys.exit(1)
    window = MainWindow()
    application.main_window = window
    window.show()
    QTimer.singleShot(1, lambda: splash_screen.finish(window))
    sys.exit(application.exec())