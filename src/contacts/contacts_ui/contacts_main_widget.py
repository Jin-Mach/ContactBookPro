from PyQt6.QtWidgets import QWidget, QLayout, QGridLayout

from src.contacts.contacts_ui.widgets.contacts_detail_widget import ContactsDetailWidget
from src.contacts.contacts_ui.widgets.contacts_statusbar_widget import ContactsStatusbarWidgte
from src.contacts.contacts_ui.widgets.contacts_tableview_widget import ContactsTableviewWidget
from src.contacts.contacts_ui.widgets.contacts_toolbar_widget import ContactsToolbarWidget
from src.database.mandatory_model import MandatoryModel
from src.database.db_connection import create_db_connection


class ContactsMainWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("contactsMainWidget")
        db_connection = create_db_connection("contacts_db.sqlite")
        self.database_model = MandatoryModel(db_connection)
        self.contacts_toolbar_widget = ContactsToolbarWidget(db_connection, self)
        self.contacts_tableview_widget = ContactsTableviewWidget(self.database_model, self)
        self.contacts_detail_widget = ContactsDetailWidget(self)
        self.contacts_statusbar_widget = ContactsStatusbarWidgte(self)
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QGridLayout()
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)
        main_layout.addWidget(self.contacts_toolbar_widget, 0, 0, 1, 2)
        main_layout.addWidget(self.contacts_tableview_widget, 1, 0)
        main_layout.addWidget(self.contacts_detail_widget, 1, 1)
        main_layout.addWidget(self.contacts_statusbar_widget, 2, 0, 1, 2)
        return main_layout