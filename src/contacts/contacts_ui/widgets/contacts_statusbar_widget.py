from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLayout

from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class ContactsStatusbarWidget(QWidget):
    def __init__(self, contacts_count: int, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("contactsStatusbarWidget")
        self.contacts_total_count = contacts_count
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
                    widget.setText(f"{ui_text[widget.objectName()]} {self.contacts_total_count}/{self.contacts_total_count}")
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_count_text(self, filter_count: int, total_count: int) -> None:
        ui_text = LanguageProvider.get_ui_text(self.objectName())
        self.count_display_label.setText(f"{ui_text[self.count_display_label.objectName()]} {filter_count}/{total_count}")