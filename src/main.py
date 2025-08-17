import sys
import time

from PyQt6.QtWidgets import QApplication, QDialog

from src.application.main_window import MainWindow
from src.utilities.app_init import application_init
from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.splash_screen import SplashScreen


def create_application() -> None:
    application = QApplication(sys.argv)
    splash_screen = SplashScreen()
    splash_screen.show()
    if not application_init(application):
        result = DialogsProvider.show_init_error_dialog("Loading error",
                                                         "Critical error: Failed to load files from the GitHub repository."
                                                         "\nCheck your internet connection."
                                                         "\nThe application will close now.")
        if result == QDialog.DialogCode.Accepted or result == QDialog.DialogCode.Rejected:
            sys.exit(1)
    QApplication.processEvents()
    window = MainWindow()
    application.main_window = window
    window.show()
    time.sleep(1)
    splash_screen.finish(window)
    sys.exit(application.exec())