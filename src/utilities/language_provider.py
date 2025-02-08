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
        with open(LanguageProvider.language_path.joinpath(LanguageProvider.get_language_code(), "ui_text.json"), "r", encoding="utf-8") as file:
            language_data = json.load(file)
        return language_data[widget_name]