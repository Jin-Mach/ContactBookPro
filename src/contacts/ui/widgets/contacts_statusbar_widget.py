from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLayout

from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class ContactsStatusbarWidgte(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("contactsStatusbarWidget")
        self.parent = parent
        self.setLayout(self.create_gui())
        self.set_ui_text()

    def create_gui(self) -> QLayout:
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.count_display_label = QLabel()
        self.count_display_label.setObjectName("countDisplayLabel")
        self.count_display_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        main_layout.addWidget(self.count_display_label)
        main_layout.addStretch()
        return main_layout

    def set_ui_text(self) -> None:
        ui_text = LanguageProvider.get_ui_text(self.objectName())
        widgets = [self.count_display_label]
        try:
            for widget in widgets:
                if widget.objectName() in ui_text:
                    widget.setText(f"{ui_text[widget.objectName()]} 0/100")
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)