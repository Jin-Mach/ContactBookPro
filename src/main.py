import os

os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-logging --log-level=3"
os.environ["QT_LOGGING_RULES"] = "qt.webengine*.debug=false;qt.webengine*.info=false"

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
    splash_screen = SplashScreen()
    splash_screen.show()
    QTimer.singleShot(0, lambda: finish_and_show(splash_screen, application, application_support_provider))
    sys.exit(application.exec())


def finish_and_show(splash_screen: SplashScreen, application: QApplication, application_support_provider: ApplicationSupportProvider) -> None:
    QApplication.processEvents()
    if not files_init(application_support_provider):
        result = DialogsProvider.show_init_error_dialog(
            "Loading error",
            "Failed to load files from the GitHub repository.\n"
            "Check your internet connection.\nThe application will close now."
        )
        if result in (QDialog.DialogCode.Accepted, QDialog.DialogCode.Rejected):
            sys.exit(1)
    if not application_init(application, application_support_provider):
        result = DialogsProvider.show_init_error_dialog(
            "Loading error",
            "Failed during application setup.\nThe application will close now."
        )
        if result in (QDialog.DialogCode.Accepted, QDialog.DialogCode.Rejected):
            sys.exit(1)
    window = MainWindow()
    application.main_window = window
    window.show()
    splash_screen.finish(window)
    window.raise_()
    window.activateWindow()