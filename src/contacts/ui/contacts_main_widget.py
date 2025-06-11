from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout, QMainWindow

from src.contacts.ui.widgets.contacts_detail_widget import ContactsDetailWidget
from src.contacts.ui.widgets.contacts_statusbar_widget import ContactsStatusbarWidget
from src.contacts.ui.widgets.contacts_tableview_widget import ContactsTableviewWidget
from src.contacts.ui.widgets.contacts_toolbar_widget import ContactsToolbarWidget
from src.database.models.completer_model import CompleterModel
from src.database.models.detail_model import DetailModel
from src.database.models.info_model import InfoModel
from src.database.models.mandatory_model import MandatoryModel
from src.database.db_connection import create_db_connection
from src.database.models.social_model import SocialModel
from src.database.models.work_model import WorkModel


class ContactsMainWidget(QWidget):
    def __init__(self, main_window: QMainWindow, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("contactsMainWidget")
        self.db_connection = create_db_connection("contacts_db.sqlite")
        self.mandatory_model = MandatoryModel(self.db_connection)
        self.work_model = WorkModel(self.db_connection)
        self.social_model = SocialModel(self.db_connection)
        self.detail_model = DetailModel(self.db_connection)
        self.info_model = InfoModel(self.db_connection)
        self.completer_model = CompleterModel(self.db_connection)
        self.contacts_detail_widget = ContactsDetailWidget(self)
        self.contacts_tableview_widget = ContactsTableviewWidget(self.mandatory_model, self.contacts_detail_widget, self)
        self.contacts_statusbar_widget = ContactsStatusbarWidget(self.mandatory_model.rowCount(), self)
        self.contacts_toolbar_widget = ContactsToolbarWidget(main_window, self.db_connection, self.mandatory_model, self.work_model,
                                                             self.social_model,self.detail_model, self.info_model,
                                                             self.contacts_detail_widget,self.contacts_tableview_widget,
                                                             self.contacts_statusbar_widget,self.completer_model, self)
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