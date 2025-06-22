import sys

from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.language_provider import LanguageProvider
from src.utilities.logger_provider import get_logger


class ErrorHandler:
    class_name = "errorHandler"
    logger = get_logger()

    @staticmethod
    def exception_handler(exception: Exception, parent=None) -> None:
        ErrorHandler.logger.error(exception, exc_info=True)
        DialogsProvider.show_error_dialog(ErrorHandler.get_error_text(exception), parent)

    @staticmethod
    def get_error_text(exception: Exception) -> str:
        try:
            errors_data = LanguageProvider.get_error_text(ErrorHandler.class_name)
            if not errors_data:
                return ""
            return errors_data.get(exception.__class__.__name__, errors_data.get("UnexpectedError", ""))
        except Exception as e:
            ErrorHandler.logger.error(f"Error getting error text: {e}", exc_info=True)
            return "Unknown error"

    @staticmethod
    def database_error(error_message: str, close_app: bool, custom_message: str | None = None) -> None:
        try:
            ErrorHandler.logger.error(error_message)
            errors_data = LanguageProvider.get_error_text(ErrorHandler.class_name) or {}
            if custom_message is not None and custom_message in errors_data:
                message = custom_message
            else:
                message = "DatabaseConnectionError"
            error = errors_data.get(message, "")
            DialogsProvider.show_database_error_dialog(error)
        except Exception as e:
            ErrorHandler.logger.error(f"Error showing database error dialog: {e}", exc_info=True)
        if close_app:
            sys.exit(1)