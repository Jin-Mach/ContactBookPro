from PyQt6.QtWidgets import QTextEdit, QWidget

from src.utilities.error_handler import ErrorHandler


def set_text_edit_state(text_edit_list: list[QTextEdit], parent: QWidget) -> None:
    try:
        for text_edit in text_edit_list:
            text_edit.setStyleSheet("font: Arial; font-size: 15spt;")
            text_edit.setReadOnly(True)
    except Exception as e:
        ErrorHandler.exception_handler(e, parent)