from PyQt6.QtWidgets import QApplication

from src.utilities.basic_setup_provider import BasicSetupProvider
from src.utilities.language_provider import LanguageProvider
from src.utilities.style_provider import StyleProvider


def application_init(application: QApplication) -> bool:
    if not BasicSetupProvider.download_files() or not StyleProvider.set_style(application):
        return False
    LanguageProvider.initialize_language()
    return True