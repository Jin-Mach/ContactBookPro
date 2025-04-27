from datetime import datetime

from PyQt6.QtWidgets import QDialog

from src.contacts.contacts_ui.dialogs.contact_dialog import ContactDialog
from src.contacts.contacts_ui.dialogs.delete_dialogs import DeleteDialogs
from src.contacts.contacts_ui.widgets.contacts_detail_widget import ContactsDetailWidget
from src.contacts.contacts_ui.widgets.contacts_statusbar_widget import ContactsStatusbarWidget
from src.contacts.contacts_ui.widgets.contacts_tableview_widget import ContactsTableviewWidget
from src.database.database_utilities.models_refresher import refresh_models
from src.database.database_utilities.reset_database import reset_database
from src.database.database_utilities.row_data_provider import RowDataProvider
from src.database.models.detail_model import DetailModel
from src.database.models.info_model import InfoModel
from src.database.models.mandatory_model import MandatoryModel
from src.database.models.social_model import SocialModel
from src.database.models.work_model import WorkModel
from src.utilities.error_handler import ErrorHandler


class ContactsController:
    def __init__(self, mandatory_model: MandatoryModel, work_model: WorkModel, social_model: SocialModel, detail_model: DetailModel,
                 info_model: InfoModel, detail_widget: ContactsDetailWidget, table_view: ContactsTableviewWidget,
                 status_bar: ContactsStatusbarWidget, parent=None) -> None:
        self.mandatory_model = mandatory_model
        self.work_model = work_model
        self.social_model = social_model
        self.detail_model = detail_model
        self.info_model = info_model
        self.detail_widget = detail_widget
        self.table_view = table_view
        self.status_bar = status_bar
        self.parent = parent

    def add_new_contact(self) -> None:
        try:
            dialog = ContactDialog(False, self.parent)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.colected_data
                if data:
                    self.mandatory_model.add_contact(data[0])
                    last_id = RowDataProvider.get_last_id(self.mandatory_model)
                    if last_id != -1:
                        self.work_model.add_contact([last_id] + data[1])
                        self.social_model.add_contact([last_id] + data[2])
                        self.detail_model.add_contact([last_id] + data[3])
                        self.info_model.add_contact([last_id] + data[4])
                        refresh_models([self.mandatory_model, self.work_model, self.social_model, self.detail_model, self.info_model])
                        self.status_bar.set_count_text(self.mandatory_model.rowCount())
                        index = self.mandatory_model.index(self.mandatory_model.rowCount() - 1, 0)
                        self.table_view.selectRow(index.row())
                        self.table_view.scrollTo(index)
                        self.table_view.contact_data_controler.get_models_data(last_id)
                    else:
                        ErrorHandler.database_error(self.mandatory_model.lastError().text(), False)
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def update_contact(self) -> None:
        try:
            index = self.table_view.selectionModel().currentIndex()
            if index.isValid():
                id_data = self.mandatory_model.index(index.row(), 0)
                contact_id = self.mandatory_model.data(id_data)
                contact_data = RowDataProvider.return_row_data(contact_id)
                dialog = ContactDialog(True, contact_data, self.parent)
                if dialog.exec() == dialog.DialogCode.Accepted:
                    update_data = dialog.colected_data
                    now = datetime.now().strftime("%d.%m.%Y")
                    self.mandatory_model.update_contact(index.row(), update_data[0])
                    self.work_model.update_contact(contact_id, update_data[1])
                    self.social_model.update_contact(contact_id, update_data[2])
                    self.detail_model.update_contact(contact_id, update_data[3])
                    self.info_model.update_contact(contact_id, now)
                    refresh_models([self.mandatory_model, self.work_model, self.social_model, self.detail_model, self.info_model])
                    self.table_view.set_detail_data(index)
            else:
                ErrorHandler.database_error(self.mandatory_model.lastError().text(), False)
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def delete_contact(self) -> None:
        try:
            index = self.table_view.selectionModel().currentIndex()
            if index.isValid():
                dialog = DeleteDialogs.show_delete_contact_dialog()
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    self.mandatory_model.delete_contact(index.row())
                    refresh_models([self.mandatory_model, self.work_model, self.social_model, self.detail_model, self.info_model])
                    self.status_bar.set_count_text(self.mandatory_model.rowCount())
                    self.detail_widget.reset_data()
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def delete_all_contacts(self) -> None:
        try:
            dialog = DeleteDialogs.show_delete_all_contacts_dialog()
            if dialog.exec() == QDialog.DialogCode.Accepted:
                if not reset_database():
                    self.mandatory_model.clear_database()
                refresh_models([self.mandatory_model, self.work_model, self.social_model, self.detail_model, self.info_model])
                self.status_bar.set_count_text(self.mandatory_model.rowCount())
                self.detail_widget.reset_data()
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)