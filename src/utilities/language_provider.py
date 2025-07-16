import json
import pathlib
import sys

from PyQt6.QtCore import QLocale


class LanguageProvider:
    language_path = pathlib.Path(__file__).parents[2].joinpath("languages")
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
    def load_json(file_name: str) -> dict | None:
        try:
            path = LanguageProvider.language_path.joinpath(LanguageProvider.language_code, file_name)
            if path.exists():
                with open(path, "r", encoding="utf-8") as file:
                    return json.load(file)
            else:
                return None
        except Exception as e:
            LanguageProvider.write_log_exception(e)
            return None

    @staticmethod
    def get_ui_text(widget_name: str) -> dict[str, str] | None:
        data = LanguageProvider.load_json("ui_text.json")
        if data:
            return data.get(widget_name)
        return None

    @staticmethod
    def get_tooltips_text(widget_name: str) -> dict[str, str] | None:
        data = LanguageProvider.load_json("tooltips_text.json")
        if data:
            return data.get(widget_name)
        return None
    
    @staticmethod
    def get_statustips_text(widget_name: str) -> dict[str, str] | None:
        data = LanguageProvider.load_json("statustips_text.json")
        if data:
            return data.get(widget_name)
        return None

    @staticmethod
    def get_dialog_text(widget_name: str) -> dict[str, str] | None:
        data = LanguageProvider.load_json("dialog_text.json")
        if data:
            return data.get(widget_name)
        return None

    @staticmethod
    def get_search_dialog_text(widget_name: str) -> dict[str, str] | None:
        data = LanguageProvider.load_json("search_dialog_text.json")
        if data:
            return data.get(widget_name)
        return None

    @staticmethod
    def get_user_filters_dialog_text(widget_name: str) -> dict[str, str] | None:
        data = LanguageProvider.load_json("user_filters_dialog_text.json")
        if data:
            return data.get(widget_name)
        return None

    @staticmethod
    def get_context_menu_text(widget_name: str) -> dict[str, str] | None:
        data = LanguageProvider.load_json("menu_text.json")
        if data:
            return data.get(widget_name)
        return None

    @staticmethod
    def get_preview_dialog_text(widget_name: str) -> dict[str, str] | None:
        data = LanguageProvider.load_json("preview_dialog_text.json")
        if data:
            return data.get(widget_name)
        return None

    @staticmethod
    def get_error_text(widget_name: str) -> dict[str, str] | None:
        data = LanguageProvider.load_json("errors_text.json")
        if data:
            return data.get(widget_name)
        return None

    @staticmethod
    def get_headers_text(widget_name: str) -> dict[str, str] | None:
        data = LanguageProvider.load_json("headers_text.json")
        if data:
            return data.get(widget_name)
        return None

    @staticmethod
    def get_export_settings(widget_name: str) -> tuple[bool, dict[str, dict[str, str]]] | None:
        data = LanguageProvider.load_json("export_settings.json")
        if data:
            semicolon = LanguageProvider.language_code[:2] in data.get("semicolon_locales", [])
            return semicolon, data.get(widget_name)
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