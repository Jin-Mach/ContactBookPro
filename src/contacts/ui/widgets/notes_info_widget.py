from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout, QTextEdit, QHBoxLayout, QLabel


class NotesInfoWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("notesInfoWidget")
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.notes_text_edit = QTextEdit()
        self.notes_text_edit.setObjectName("notestextEdit")
        self.notes_text_edit.setReadOnly(True)
        self.notes_text_edit.setText("some note text")
        notes_date_layout = QHBoxLayout()
        notes_date_layout.setContentsMargins(0, 0, 0, 0)
        notes_date_layout.setSpacing(0)
        self.create_date_text_label = QLabel("create:")
        self.create_date_text_label.setObjectName("createDatetextLabel")
        self.create_date_label = QLabel("1.1.2025")
        self.create_date_label.setObjectName("createdateLabel")
        self.update_date_text_label = QLabel("update:")
        self.update_date_text_label.setObjectName("updateDatetextLabel")
        self.update_date_label = QLabel("31.12.2025")
        self.update_date_label.setObjectName("updateDateLabel")
        notes_date_layout.addWidget(self.create_date_text_label)
        notes_date_layout.addWidget(self.create_date_label)
        notes_date_layout.addStretch()
        notes_date_layout.addWidget(self.update_date_text_label)
        notes_date_layout.addWidget(self.update_date_label)
        main_layout.addWidget(self.notes_text_edit)
        main_layout.addLayout(notes_date_layout)
        return main_layout