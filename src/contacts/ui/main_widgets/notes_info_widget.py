from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout, QTextEdit, QHBoxLayout, QLabel

from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class NotesInfoWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("notesInfoWidget")
        self.setLayout(self.create_gui())
        self.set_ui_text()

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.notes_text_edit = QTextEdit()
        self.notes_text_edit.setObjectName("notesTextEdit")
        self.notes_text_edit.setReadOnly(True)
        self.notes_text_edit.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        notes_date_layout = QHBoxLayout()
        notes_date_layout.setContentsMargins(0, 0, 0, 0)
        notes_date_layout.setSpacing(0)
        self.create_date_text_label = QLabel()
        self.create_date_text_label.setObjectName("createDateTextLabel")
        self.create_date_label = QLabel()
        self.create_date_label.setObjectName("createdateLabel")
        self.update_date_text_label = QLabel()
        self.update_date_text_label.setObjectName("updateDateTextLabel")
        self.update_date_label = QLabel()
        self.update_date_label.setObjectName("updateDateLabel")
        notes_date_layout.addWidget(self.create_date_text_label)
        notes_date_layout.addWidget(self.create_date_label)
        notes_date_layout.addStretch()
        notes_date_layout.addWidget(self.update_date_text_label)
        notes_date_layout.addWidget(self.update_date_label)
        main_layout.addWidget(self.notes_text_edit)
        main_layout.addLayout(notes_date_layout)
        return main_layout

    def set_ui_text(self) -> None:
        ui_text = LanguageProvider.get_ui_text(self.objectName())
        widgets = [self.notes_text_edit, self.create_date_text_label, self.update_date_text_label]
        try:
            for widget in widgets:
                if widget.objectName() in ui_text:
                    if isinstance(widget, QTextEdit):
                        widget.setPlaceholderText(ui_text[widget.objectName()])
                    elif isinstance(widget, QLabel):
                        widget.setText(ui_text[widget.objectName()])
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_data(self, data: dict) -> None:
        try:
            self.notes_text_edit.setPlainText(data["notes"])
            self.create_date_label.setText(data["created"])
            self.update_date_label.setText(data["updated"])
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def reset_data(self) -> None:
        widgets = [self.notes_text_edit, self.create_date_label, self.update_date_label]
        for widget in widgets:
            widget.clear()