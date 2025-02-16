import sys

from PyQt6.QtWidgets import QApplication, QDialog

from src.main_window.main_window import MainWindow
from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.language_provider import LanguageProvider
from src.utilities.style_provider import StyleProvider


def create_application() -> None:
    application = QApplication(sys.argv)
    StyleProvider.set_style(application)
    missing_files = LanguageProvider.check_text_files()
    if missing_files:
        result = DialogsProvider.show_language_error_dialog(missing_files)
        if result == QDialog.DialogCode.Rejected:
            sys.exit(1)
    window = MainWindow()
    window.show()
    sys.exit(application.exec())