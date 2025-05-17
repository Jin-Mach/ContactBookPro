import sys
from typing import Optional

from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.language_provider import LanguageProvider
from src.utilities.logger_provider import get_logger


class ErrorHandler:
    class_name = "errorHandler"
    logger = get_logger()

    @staticmethod
    def exception_handler(exception: Exception, parent=None) -> None:
        ErrorHandler.logger.error(exception, exc_info=True)
        DialogsProvider.show_error_dialog(ErrorHandler.get_error_text(exception))

    @staticmethod
    def get_error_text(exception: Exception) -> str:
        errors_data = LanguageProvider.get_error_text(ErrorHandler.class_name)
        if exception.__class__.__name__ not in errors_data:
            return errors_data["UnexpectedError"]
        return errors_data[exception.__class__.__name__]

    @staticmethod
    def database_error(error_message: str, close_app: bool, custom_message: Optional[str] = None) -> None:
        ErrorHandler.logger.error(error_message)
        if custom_message is not None and custom_message in LanguageProvider.get_error_text(ErrorHandler.class_name):
            message = custom_message
        else:
            message = "DatabaseConnectionError"
        error = LanguageProvider.get_error_text(ErrorHandler.class_name)[message]
        DialogsProvider.show_database_error_dialog(error)
        if close_app:
            sys.exit(1)
        else:
            pass