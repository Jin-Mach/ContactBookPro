from typing import TYPE_CHECKING

from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout, QMainWindow

from src.contacts.ui.main_widgets.contacts_detail_widget import ContactsDetailWidget
from src.contacts.ui.main_widgets.contacts_statusbar_widget import ContactsStatusBarWidget
from src.contacts.ui.main_widgets.contacts_tableview_widget import ContactsTableviewWidget
from src.contacts.ui.main_widgets.contacts_toolbar_widget import ContactsToolbarWidget
from src.database.models.completer_model import CompleterModel
from src.database.models.detail_model import DetailModel
from src.database.models.info_model import InfoModel
from src.database.models.social_model import SocialModel
from src.database.models.work_model import WorkModel

if TYPE_CHECKING:
    from src.map.controllers.map_controller import MapController
    from src.statistics.controllers.statistics_controller import StatisticsController
    from src.database.models.mandatory_model import MandatoryModel


class ContactsMainWidget(QWidget):
    def __init__(self, db_connection: QSqlDatabase, mandatory_model: "MandatoryModel",main_window: QMainWindow,
                 map_controller: "MapController", statistics_controller: "StatisticsController",
                 parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("contactsMainWidget")
        self.db_connection = db_connection
        self.mandatory_model = mandatory_model
        self.map_controller = map_controller
        self.statistics_controller = statistics_controller
        self.work_model = WorkModel(self.db_connection)
        self.social_model = SocialModel(self.db_connection)
        self.detail_model = DetailModel(self.db_connection)
        self.info_model = InfoModel(self.db_connection)
        self.completer_model = CompleterModel(self.db_connection)
        self.contacts_detail_widget = ContactsDetailWidget(self)
        self.contacts_statusbar_widget = ContactsStatusBarWidget(self.mandatory_model.rowCount(), self)
        self.contacts_tableview_widget = ContactsTableviewWidget(self.mandatory_model, self.contacts_detail_widget,
                                                                 self.contacts_statusbar_widget, self)
        self.contacts_toolbar_widget = ContactsToolbarWidget(main_window, self.db_connection, self.mandatory_model, self.work_model,
                                                             self.social_model,self.detail_model, self.info_model,
                                                             self.contacts_detail_widget,self.contacts_tableview_widget,
                                                             self.contacts_statusbar_widget,self.completer_model,
                                                             self.map_controller, self.statistics_controller, self)
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