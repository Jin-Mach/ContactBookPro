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
            from error_handler import ErrorHandler
            ErrorHandler.exception_handler(e)
            return {}

    @staticmethod
    def get_dialog_text(widget_name: str) -> dict[str, str]:
        try:
            with open(LanguageProvider.language_path.joinpath(LanguageProvider.get_language_code(), "dialog_text.json"), "r", encoding="utf-8") as file:
                dialog_data = json.load(file)
            return dialog_data[widget_name]
        except Exception as e:
            from error_handler import ErrorHandler
            ErrorHandler.exception_handler(e)
            return {}

    @staticmethod
    def get_error_text(widget_name: str) -> dict[str, str]:
        try:
            with open(LanguageProvider.language_path.joinpath(LanguageProvider.get_language_code(), "errors_text.json"), "r", encoding="utf-8") as file:
                error_data = json.load(file)
            return error_data[widget_name]
        except Exception as e:
            from error_handler import ErrorHandler
            ErrorHandler.exception_handler(e)
            return {}