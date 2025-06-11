import webbrowser

from PyQt6.QtWidgets import QPushButton

from src.utilities.error_handler import ErrorHandler


def open_url(url: str, parent=None) -> None:
    try:
        if not webbrowser.open_new_tab(url):
            if not webbrowser.open_new(url):
                if not webbrowser.open(url):
                    raise RuntimeError
    except Exception as e:
        ErrorHandler.exception_handler(e, parent)

def update_buttons_state(buttons: list[QPushButton], urls: list[str | None]) -> None:
    for button, url in zip(buttons, urls):
        button.setDisabled(not url)