import sys

from PyQt6.QtWidgets import QApplication, QDialog

from src.application.main_window import MainWindow
from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.basic_setup_provider import BasicSetupProvider
from src.utilities.style_provider import StyleProvider


def create_application() -> None:
    application = QApplication(sys.argv)
    if not BasicSetupProvider.download_files():
        result = DialogsProvider.show_files_error_dialog()
        if result == QDialog.DialogCode.Accepted or result == QDialog.DialogCode.Rejected:
            sys.exit(1)
    StyleProvider.set_style(application)
    window = MainWindow()
    window.show()
    sys.exit(application.exec())