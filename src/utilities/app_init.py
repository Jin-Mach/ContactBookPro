from PyQt6.QtWidgets import QApplication

from src.utilities.basic_setup_provider import BasicSetupProvider
from src.utilities.language_provider import LanguageProvider
from src.utilities.style_provider import set_application_style


def application_init(application: QApplication) -> bool:
    if not BasicSetupProvider.download_files():
        return False
    application.setStyle("Fusion")
    set_application_style(application)
    LanguageProvider.initialize_language()
    return True