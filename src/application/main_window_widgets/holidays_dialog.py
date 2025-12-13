from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QLabel, QTextEdit, QDialogButtonBox


class HolidaysDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("HolidaysDialog")
        self.create_gui()

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
        main_layout.addWidget(self.holiday_date_label)
        main_layout.addWidget(self.holiday_text_label)
        main_layout.addWidget(self.holiday_info_label)
        main_layout.addWidget(button_box)
        return main_layout