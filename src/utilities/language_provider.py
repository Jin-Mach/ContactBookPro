import pathlib
import json
import sys
from typing import Optional

from PyQt6.QtCore import QLocale


class LanguageProvider:
    language_path = pathlib.Path(__file__).parent.parent.joinpath("languages")
    language_code = None

    @staticmethod
    def initialize_language() -> str:
        return LanguageProvider.get_language_code()

    @staticmethod
    def get_language_code() -> Optional[str]:
        try:
            language = QLocale().name()
            if not LanguageProvider.language_code or not language:
                language_dict = LanguageProvider.get_language_dict()
                if language not in language_dict:
                    from src.utilities.dialogs_provider import DialogsProvider
                    result = DialogsProvider.language_selection_dialog(list(language_dict.values()))
                    if result:
                        for language_code, language_name in language_dict.items():
                            if result == language_name:
                                LanguageProvider.language_code = language_code
                    else:
                        sys.exit(1)
                else:
                    LanguageProvider.language_code = language
            return LanguageProvider.language_code
        except Exception as e:
            LanguageProvider.write_log_exception(e)
            return None

    @staticmethod
    def get_ui_text(widget_name: str) -> Optional[dict[str, str]]:
        try:
            with open(LanguageProvider.language_path.joinpath(LanguageProvider.language_code, "ui_text.json"), "r", encoding="utf-8") as file:
                language_data = json.load(file)
            return language_data[widget_name]
        except Exception as e:
            LanguageProvider.write_log_exception(e)
            return None

    @staticmethod
    def get_dialog_text(widget_name: str) -> Optional[dict[str, str]]:
        try:
            with open(LanguageProvider.language_path.joinpath(LanguageProvider.language_code, "dialog_text.json"), "r", encoding="utf-8") as file:
                dialog_data = json.load(file)
            return dialog_data[widget_name]
        except Exception as e:
            LanguageProvider.write_log_exception(e)
            return None


    @staticmethod
    def get_error_text(widget_name: str) -> Optional[dict[str, str]]:
        try:
            with open(LanguageProvider.language_path.joinpath(LanguageProvider.language_code, "errors_text.json"), "r", encoding="utf-8") as file:
                error_data = json.load(file)
            return error_data[widget_name]
        except Exception as e:
            LanguageProvider.write_log_exception(e)
            return None

    @staticmethod
    def get_headers_text(widget_name: str) -> Optional[dict[str, str]]:
        try:
            with open(LanguageProvider.language_path.joinpath(LanguageProvider.language_code, "headers_text.json"), "r", encoding="utf-8") as file:
                headers_data = json.load(file)
            return headers_data[widget_name]
        except Exception as e:
            LanguageProvider.write_log_exception(e)
            return None

    @staticmethod
    def get_language_dict() -> Optional[dict]:
        language_dict = {}
        try:
            for language in LanguageProvider.language_path.iterdir():
                if language.is_dir():
                    with open(language.joinpath("language_info.json"), "r", encoding="utf-8") as file:
                        language_text = json.load(file)
                    language_dict[language.name] = list(language_text.values())[0]
            return language_dict
        except Exception as e:
            LanguageProvider.write_log_exception(e)
            return None

    @staticmethod
    def write_log_exception(exception: Exception) -> None:
        from src.utilities.logger_provider import get_logger
        logger = get_logger()
        logger.error(exception, exc_info=True)