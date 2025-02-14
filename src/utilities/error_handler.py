from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.language_provider import LanguageProvider
from src.utilities.logger_provider import get_logger


class ErrorHandler:
    class_name = "errorHandler"

    @staticmethod
    def exception_handler(exception: Exception, parent=None) -> None:
        logger = get_logger()
        logger.error(exception, exc_info=True)
        DialogsProvider.show_error_dialog(ErrorHandler.get_error_text(exception), parent)

    @staticmethod
    def get_error_text(exception: Exception) -> str:
        errors_data = LanguageProvider.get_error_text(ErrorHandler.class_name)
        if exception.__class__.__name__ not in errors_data:
            return errors_data["UnexpectedError"]
        return errors_data[exception.__class__.__name__]