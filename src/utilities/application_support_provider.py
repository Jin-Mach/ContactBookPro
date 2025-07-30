import json
import os
import sys
import requests

from qt_material import apply_stylesheet

from PyQt6.QtWidgets import QApplication

from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class ApplicationSupportProvider:

    @staticmethod
    def connection_result() -> bool:
        try:
            response = requests.get(url="https://github.com", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    @staticmethod
    def restart_application() -> None:
        os.execv(sys.executable, [sys.executable, sys.argv[0]] + sys.argv[1:])

    @staticmethod
    def get_encoding() -> str:
        encoding = "utf-8"
        if sys.platform.startswith("win"):
            encoding = "cp1250"
        return encoding

    @staticmethod
    def set_application_style(application: QApplication) -> None:
        apply_stylesheet(application, "dark_blue.xml")

    @staticmethod
    def get_default_location() -> dict | None:
        try:
            application_language = LanguageProvider.language_code
            language_path = LanguageProvider.language_path
            path = language_path.joinpath(application_language, "language_setup.json")
            if path.exists():
                with open(path, "r", encoding="utf-8") as file:
                    return json.load(file)
            return None
        except Exception as e:
            ErrorHandler.exception_handler(e)
            return None