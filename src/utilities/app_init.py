from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QApplication, QDialog

from src.threading.download_files_object import DownloadFilesObject
from src.utilities.dialogs_provider import DownloadFilesDialog
from src.utilities.files_provider import FilesProvider
from src.utilities.language_provider import LanguageProvider
from src.utilities.logger_provider import get_logger

if TYPE_CHECKING:
    from src.utilities.application_support_provider import ApplicationSupportProvider


logger = get_logger()

def files_init(application_support_provider: "ApplicationSupportProvider") -> bool:
    try:
        files_provider = FilesProvider()
        download_files_object = DownloadFilesObject(files_provider, application_support_provider)
        missing_files = download_files_object.get_missing_files()
        if not missing_files:
            return True
        dialog = DownloadFilesDialog(download_files_object)
        result = dialog.exec()
        return result == QDialog.DialogCode.Accepted
    except Exception as e:
        logger.exception(f"{files_init} {'Exception during application initialization'}: {e}", exc_info=True)
        return False

def application_init(application: QApplication, application_support_provider: "ApplicationSupportProvider") -> bool:
    try:
        application.setStyle("Fusion")
        application_support_provider.set_application_style(application)
        LanguageProvider.initialize_language()
        return True
    except Exception as e:
        if isinstance(e, (SystemExit, KeyboardInterrupt)):
            raise
        logger.exception(f"{application_init} {'Exception during application initialization'}: {e}", exc_info=True)
        return False