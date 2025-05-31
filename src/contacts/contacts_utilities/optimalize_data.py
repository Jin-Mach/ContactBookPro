import unicodedata
from PyQt6.QtWidgets import QLineEdit, QTextEdit


def normalize_texts(inputs: list[QLineEdit | QTextEdit]) -> list:
    normalized_list = []
    for user_input in inputs:
        if isinstance(user_input, QLineEdit):
            text = user_input.text().lower()
            normalized_list.append(unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8"))
        elif isinstance(user_input, QTextEdit):
            text = user_input.toPlainText().lower()
            normalized_list.append(unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8"))
    return normalized_list