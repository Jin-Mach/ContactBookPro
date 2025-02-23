import pathlib
import json

from PyQt6.QtCore import QLocale


class LanguageProvider:
    language_path = pathlib.Path(__file__).parent.parent.joinpath("languages")

    @staticmethod
    def get_language_code() -> str:
        language = QLocale().name()
        return language

    @staticmethod
    def get_ui_text(widget_name: str) -> dict[str, str]:
        try:
            with open(LanguageProvider.language_path.joinpath(LanguageProvider.get_language_code(), "ui_text.json"), "r", encoding="utf-8") as file:
                language_data = json.load(file)
            return language_data[widget_name]
        except Exception as e:
            LanguageProvider.write_log_exception(e)
            return {}

    @staticmethod
    def get_dialog_text(widget_name: str) -> dict[str, str]:
        try:
            with open(LanguageProvider.language_path.joinpath(LanguageProvider.get_language_code(), "dialog_text.json"), "r", encoding="utf-8") as file:
                dialog_data = json.load(file)
            return dialog_data[widget_name]
        except Exception as e:
            LanguageProvider.write_log_exception(e)
            return {}


    @staticmethod
    def get_error_text(widget_name: str) -> dict[str, str]:
        try:
            with open(LanguageProvider.language_path.joinpath(LanguageProvider.get_language_code(), "errors_text.json"), "r", encoding="utf-8") as file:
                error_data = json.load(file)
            return error_data[widget_name]
        except Exception as e:
            LanguageProvider.write_log_exception(e)
            return {}

    @staticmethod
    def get_headers_text(widget_name: str) -> dict[str, str]:
        try:
            with open(LanguageProvider.language_path.joinpath(LanguageProvider.get_language_code(), "headers_text.json"), "r", encoding="utf-8") as file:
                headers_data = json.load(file)
            return headers_data[widget_name]
        except Exception as e:
            LanguageProvider.write_log_exception(e)
            return {}

    @staticmethod
    def write_log_exception(exception: Exception) -> None:
        from src.utilities.logger_provider import get_logger
        logger = get_logger()
        logger.error(exception, exc_info=True)

    @staticmethod
    def check_text_files() -> list:
        required_files = ["dialog_text.json", "errors_text.json", "ui_text.json"]
        files_path = LanguageProvider.language_path.joinpath(LanguageProvider.get_language_code())
        missing_files = []
        for file in required_files:
            file_path = files_path.joinpath(file)
            if not file_path.exists() or not file_path.is_file():
                missing_files.append(file)
        return missing_files