from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import QTextEdit, QLabel

from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


def check_notes_length(notes_edit: QTextEdit, count_label: QLabel, parent=None) -> None:
    try:
        max_chars = 300
        max_lines = 10
        text = notes_edit.toPlainText()
        lines = text.splitlines()
        error_text = LanguageProvider.get_json_text("errors_text.json", "notesUtilities")
        if len(lines) > max_lines:
            trimmed_text = "\n".join(lines[:max_lines])
            notes_edit.setPlainText(trimmed_text)
            if error_text:
                DialogsProvider.show_error_dialog(error_text.get("textLineCountError", parent))
        elif len(text) > max_chars:
            notes_edit.setPlainText(text[:max_chars])
            if error_text:
                DialogsProvider.show_error_dialog(error_text.get("textLengthError", parent))
        cursor = notes_edit.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        notes_edit.setTextCursor(cursor)
        updated_text = notes_edit.toPlainText()
        count_label.setText(f"{len(updated_text)}/{max_chars}")
    except Exception as e:
        ErrorHandler.exception_handler(e, parent)
