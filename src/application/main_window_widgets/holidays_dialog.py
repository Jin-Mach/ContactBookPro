import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QLabel, QTextEdit, QDialogButtonBox

from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class HolidaysDialog(QDialog):
    def __init__(self, holidays_data: tuple[datetime.date, str] | None, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("holidaysDialog")
        self.setMinimumSize(400, 350)
        self.holidays_data = holidays_data
        print(self.holidays_data)
        self.setLayout(self.create_gui())
        self.set_ui_text()

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.holiday_date_label = QLabel()
        self.holiday_date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.holiday_text_label = QLabel()
        self.holiday_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.holiday_info_label = QTextEdit()
        self.holiday_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.holiday_info_label.setReadOnly(True)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(self.reject)
        self.close_button = button_box.button(QDialogButtonBox.StandardButton.Close)
        self.close_button.setObjectName("closeButton")
        main_layout.addWidget(self.holiday_date_label)
        main_layout.addWidget(self.holiday_text_label)
        main_layout.addWidget(self.holiday_info_label)
        main_layout.addWidget(button_box)
        return main_layout

    def set_ui_text(self) -> None:
        try:
            ui_text = LanguageProvider.get_json_text("dialog_text.json", self.objectName())
            if ui_text:
                if "holidaysDialogTitle" in ui_text:
                    self.setWindowTitle(ui_text.get("holidaysDialogTitle", ""))
                self.close_button.setText(ui_text.get("closeButton", ""))
        except Exception as e:
            ErrorHandler.exception_handler(e)