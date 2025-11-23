import sys

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import QApplication, QDialog, QSplashScreen

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
    window.hide()
    application.main_window = window
    QTimer.singleShot(200, lambda: finish_and_show(splash_screen, window))
    sys.exit(application.exec())

def finish_and_show(splash_screen: QSplashScreen, main_window: MainWindow) -> None:
    splash_screen.finish(main_window)
    main_window.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint)
    main_window.show()
    main_window.raise_()
    main_window.activateWindow()
    QTimer.singleShot(300, lambda: (main_window.setWindowFlags(Qt.WindowType.Window),main_window.show()))
    QTimer.singleShot(100, lambda: main_window.raise_())