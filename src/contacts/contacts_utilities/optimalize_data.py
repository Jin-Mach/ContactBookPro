import unicodedata
from PyQt6.QtWidgets import QLineEdit, QTextEdit


def normalize_texts(inputs: list[QLineEdit | QTextEdit]) -> list:
    normalized_list = []
    for user_input in inputs:
        if isinstance(user_input, QLineEdit):
            text = user_input.text().strip().lower()
            normalized_list.append(unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8"))
        elif isinstance(user_input, QTextEdit):
            text = user_input.toPlainText().strip().lower()
            normalized_list.append(unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8"))
    return normalized_list

def normalize_input(input_widget: QLineEdit | QTextEdit) -> str:
    normalized_text = None
    if isinstance(input_widget, QLineEdit):
        text = input_widget.text().strip().lower()
        normalized_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    elif isinstance(input_widget, QTextEdit):
        text = input_widget.toPlainText().strip().lower()
        normalized_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    return normalized_text