import datetime
import json
import os
import pathlib
import sys
import requests
import holidays

from qt_material import apply_stylesheet

from PyQt6.QtWidgets import QApplication

from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class ApplicationSupportProvider:

    @staticmethod
    def get_local_holidays() -> tuple[datetime.date, str] | None:
        try:
            languages_path = pathlib.Path(__file__).parents[2].joinpath("languages")
            languages_folder = []
            for folder in languages_path.iterdir():
                if folder.is_dir():
                    languages_folder.append(str(folder.name))
            if not languages_folder:
                return None
            language = str(LanguageProvider.language_code)
            if not language in languages_folder:
                return None
            current_date = datetime.date.today()
            local_holidays = holidays.country_holidays(country=language.split("_")[1], years=[current_date.year])
            current_holidays = local_holidays.get(datetime.date(2025, 12, 24))
            if not current_holidays:
                return None
            return current_date, current_holidays
        except Exception as e:
            ErrorHandler.exception_handler(e)
            return None

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

    @staticmethod
    def hide_mac_traceback(debug: bool) -> None:
        if not debug and sys.platform == "darwin":
            sys.stderr = open(os.devnull, "w")