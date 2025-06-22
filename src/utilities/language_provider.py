import json
import pathlib
import sys

from PyQt6.QtCore import QLocale


class LanguageProvider:
    language_path = pathlib.Path(__file__).parent.parent.joinpath("languages")
    language_code = None

    @staticmethod
    def initialize_language() -> str:
        return LanguageProvider.get_language_code()

    @staticmethod
    def get_language_code() -> str | None:
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
    def get_ui_text(widget_name: str) -> dict[str, str] | None:
        try:
            with open(LanguageProvider.language_path.joinpath(LanguageProvider.language_code, "ui_text.json"), "r", encoding="utf-8") as file:
                language_data = json.load(file)
            return language_data.get(widget_name)
        except Exception as e:
            LanguageProvider.write_log_exception(e)
            return None

    @staticmethod
    def get_tooltips_text(widget_name: str) -> dict[str, str] | None:
        try:
            with open(LanguageProvider.language_path.joinpath(LanguageProvider.language_code, "tooltips_text.json"), encoding="utf-8") as file:
                tooltips_data = json.load(file)
            return tooltips_data.get(widget_name)
        except Exception as e:
            LanguageProvider.write_log_exception(e)
            return None

    @staticmethod
    def get_dialog_text(widget_name: str) -> dict[str, str] | None:
        try:
            with open(LanguageProvider.language_path.joinpath(LanguageProvider.language_code, "dialog_text.json"), "r", encoding="utf-8") as file:
                dialog_data = json.load(file)
            return dialog_data.get(widget_name)
        except Exception as e:
            LanguageProvider.write_log_exception(e)
            return None

    @staticmethod
    def get_search_dialog_text(widget_name: str) -> dict[str, str] | None:
        try:
            with open(LanguageProvider.language_path.joinpath(LanguageProvider.language_code, "search_dialog_text.json"), "r", encoding="utf-8") as file:
                search_dialog_data = json.load(file)
            return search_dialog_data.get(widget_name)
        except Exception as e:
            LanguageProvider.write_log_exception(e)
            return None

    @staticmethod
    def get_user_filters_dialog_text(widget_name: str) -> dict[str, str] | None:
        try:
            with open(LanguageProvider.language_path.joinpath(LanguageProvider.language_code, "user_filters_dialog_text.json"), "r", encoding="utf-8") as file:
                search_dialog_data = json.load(file)
            return search_dialog_data.get(widget_name)
        except Exception as e:
            LanguageProvider.write_log_exception(e)
            return None

    @staticmethod
    def get_context_menu_text(widget_name: str) -> dict[str, str] | None:
        try:
            with open(LanguageProvider.language_path.joinpath(LanguageProvider.language_code, "menu_text.json"), "r", encoding="utf-8") as file:
                context_menu_data = json.load(file)
            return context_menu_data.get(widget_name)
        except Exception as e:
            LanguageProvider.write_log_exception(e)
            return None

    @staticmethod
    def get_error_text(widget_name: str) -> dict[str, str] | None:
        try:
            with open(LanguageProvider.language_path.joinpath(LanguageProvider.language_code, "errors_text.json"), "r", encoding="utf-8") as file:
                error_data = json.load(file)
            return error_data.get(widget_name)
        except Exception as e:
            LanguageProvider.write_log_exception(e)
            return None

    @staticmethod
    def get_headers_text(widget_name: str) -> dict[str, str] | None:
        try:
            with open(LanguageProvider.language_path.joinpath(LanguageProvider.language_code, "headers_text.json"), "r", encoding="utf-8") as file:
                headers_data = json.load(file)
            return headers_data.get(widget_name)
        except Exception as e:
            LanguageProvider.write_log_exception(e)
            return None

    @staticmethod
    def get_export_settings(widget_name: str) -> tuple[bool, dict[str, dict[str, str]]] | None:
        try:
            with open(LanguageProvider.language_path.joinpath(LanguageProvider.language_code, "export_settings.json"), "r", encoding="utf-8") as file:
                index_map = json.load(file)
            semicolon = LanguageProvider.language_code[:2] in index_map["semicolon_locales"]
            return semicolon, index_map.get(widget_name)
        except Exception as e:
            LanguageProvider.write_log_exception(e)
            return None

    @staticmethod
    def get_language_dict() -> dict | None:
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