import os
import sys
import requests

from qt_material import apply_stylesheet

from PyQt6.QtWidgets import QApplication


class ApplicationSupportProvider:

    @staticmethod
    def connection_result() -> bool:
        try:
            response = requests.get(url="https://www.google.com", timeout=5)
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
