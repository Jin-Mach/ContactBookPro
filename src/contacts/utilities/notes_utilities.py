from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import QTextEdit, QLabel

from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


def check_notes_length(notes_edit: QTextEdit, count_label: QLabel, parent=None) -> None:
    try:
        text = notes_edit.toPlainText()
        error_text = LanguageProvider.get_error_text("notesUtilities")
        if len(text) > 500:
            cursor = notes_edit.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            notes_edit.setTextCursor(cursor)
            cursor.deletePreviousChar()
            if error_text:
                DialogsProvider.show_error_dialog(error_text.get("textLengthError", ""))
        else:
            count_label.setText(f"{len(text)}/500")
    except Exception as e:
        ErrorHandler.exception_handler(e, parent)