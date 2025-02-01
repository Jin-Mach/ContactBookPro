from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLayout


class ContactsStatusbarWidgte(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("contactsStatusbarWidget")
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.count_display_label = QLabel("displayed: 20/100")
        self.count_display_label.setObjectName("countDisplayLabel")
        self.count_display_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        main_layout.addWidget(self.count_display_label)
        main_layout.addStretch()
        return main_layout
