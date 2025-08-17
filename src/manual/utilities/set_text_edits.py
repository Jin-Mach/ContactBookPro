from PyQt6.QtWidgets import QTextEdit, QWidget

from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


def initialize_text_edits(text_edit_list: list[QTextEdit], parent: QWidget) -> None:
    try:
        edit_names = []
        for text_edit in text_edit_list:
            edit_names.append(text_edit.objectName())
        text = LanguageProvider.get_document_text("manual", edit_names)
        for text_edit in text_edit_list:
            text_edit.setPlainText(text.get(text_edit.objectName(), ""))
            text_edit.setStyleSheet("font: Arial; font-size: 15pt;")
            text_edit.setReadOnly(True)
    except Exception as e:
        ErrorHandler.exception_handler(e, parent)