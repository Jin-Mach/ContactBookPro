import pathlib

from PyQt6.QtWidgets import QApplication

class Stylemanager:

    @staticmethod
    def set_style(application: QApplication) -> None:
        styles_path = pathlib.Path(__file__).parent.parent.joinpath("styles", "light_blue_style.qss")
        try:
            if styles_path.exists():
                with open(styles_path, "r", encoding="utf-8") as file:
                    application.setStyleSheet(file.read())
        except Exception as e:
            print(e)