from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout

from src.contacts.contacts_ui.widgets.contacts_detail_widget import ContactsDetailWidget
from src.contacts.contacts_ui.widgets.contacts_statusbar_widget import ContactsStatusbarWidgte
from src.contacts.contacts_ui.widgets.contacts_tableview_widget import ContactsTableviewWidget
from src.contacts.contacts_ui.widgets.contacts_toolbar_widget import ContactsToolbarWidget
from src.database.models.mandatory_model import MandatoryModel
from src.database.db_connection import create_db_connection


class ContactsMainWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("contactsMainWidget")
        db_connection = create_db_connection("contacts_db.sqlite")
        self.mandatory_model = MandatoryModel(db_connection)
        self.contacts_tableview_widget = ContactsTableviewWidget(self.mandatory_model, self)
        self.contacts_toolbar_widget = ContactsToolbarWidget(self.mandatory_model, self.contacts_tableview_widget, self)
        self.contacts_detail_widget = ContactsDetailWidget(self)
        self.contacts_statusbar_widget = ContactsStatusbarWidgte(self)
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)
        main_layout.addWidget(self.contacts_toolbar_widget)
        main_layout.addWidget(self.contacts_detail_widget)
        main_layout.addWidget(self.contacts_tableview_widget)
        main_layout.addWidget(self.contacts_statusbar_widget)
        return main_layout