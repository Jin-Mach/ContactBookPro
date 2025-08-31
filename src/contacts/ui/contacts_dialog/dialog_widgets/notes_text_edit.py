from typing import Callable

from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtGui import QTextCharFormat, QColor

from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class NotesTextEdit(QTextEdit):
    def __init__(self, check_text_length: Callable[[], None], parent=None):
        super().__init__(parent)
        self.setObjectName("notesTextEdit")
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.check_text_length = check_text_length
        self.textChanged.connect(check_text_length)
        self.set_ui_text()

    def set_ui_text(self) -> None:
        try:
            ui_text = LanguageProvider.get_json_text("dialog_text.json", self.objectName())
            if ui_text:
                self.setPlaceholderText(ui_text.get("notesPlaceholderText", ""))
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def insertFromMimeData(self, source: QMimeData) -> None:
        if not source.hasText():
            super().insertFromMimeData(source)
        cursor = self.textCursor()
        char_format = QTextCharFormat()
        char_format.setForeground(QColor("#448aff"))
        cursor.insertText(source.text(), char_format)