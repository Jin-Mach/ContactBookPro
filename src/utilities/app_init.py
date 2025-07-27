from PyQt6.QtWidgets import QApplication

from src.utilities.basic_setup_provider import BasicSetupProvider
from src.utilities.language_provider import LanguageProvider
from src.utilities.logger_provider import get_logger
from src.utilities.application_support_provider import ApplicationSupportProvider


def application_init(application: QApplication) -> bool:
    try:
        BasicSetupProvider.download_files()
        application.setStyle("Fusion")
        ApplicationSupportProvider.set_application_style(application)
        LanguageProvider.initialize_language()
        return True
    except Exception as e:
        if isinstance(e, (SystemExit, KeyboardInterrupt)):
            raise
        logger = get_logger()
        logger.exception("Exception during application initialization")
        return False