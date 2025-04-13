from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout

from src.contacts.contacts_ui.widgets.notes_info_widget import NotesInfoWidget
from src.contacts.contacts_ui.widgets.personal_info_widget import PersonalInfoWidget
from src.contacts.contacts_ui.widgets.tab_info_widget import TabInfoWidget


class ContactsDetailWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("contactsDetailWidget")
        self.setFixedWidth(350)
        self.personal_info_widget = PersonalInfoWidget(self)
        self.tab_info_widget = TabInfoWidget(self)
        self.notes_info_widget = NotesInfoWidget(self)
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(5)
        main_layout.addWidget(self.personal_info_widget)
        main_layout.addWidget(self.tab_info_widget)
        main_layout.addWidget(self.notes_info_widget)
        return main_layout