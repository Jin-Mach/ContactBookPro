from PyQt6.QtWidgets import QDialog

from src.contacts.contacts_ui.dialogs.contact_dialog import ContactDialog
from src.contacts.contacts_ui.dialogs.delete_dialogs import DeleteDialogs
from src.contacts.contacts_ui.widgets.contacts_statusbar_widget import ContactsStatusbarWidget
from src.contacts.contacts_ui.widgets.contacts_tableview_widget import ContactsTableviewWidget
from src.database.models.detail_model import DetailModel
from src.database.models.info_model import InfoModel
from src.database.models.mandatory_model import MandatoryModel
from src.database.models.social_model import SocialModel
from src.database.models.work_model import WorkModel
from src.utilities.error_handler import ErrorHandler


class ContactsControler:
    def __init__(self, mandatory_model: MandatoryModel, work_model: WorkModel, social_model: SocialModel, detail_model: DetailModel,
                 info_model: InfoModel, table_view: ContactsTableviewWidget, status_bar: ContactsStatusbarWidget) -> None:
        self.mandatory_model = mandatory_model
        self.work_model = work_model
        self.social_model = social_model
        self.detail_model = detail_model
        self.info_model = info_model
        self.table_view = table_view
        self.status_bar = status_bar

    def add_new_contact(self) -> None:
        try:
            dialog = ContactDialog()
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.new_data()
                if data:
                    self.mandatory_model.add_contact(data[0])
                    last_id = self.mandatory_model.get_last_id()
                    if last_id != -1:
                        self.work_model.add_contact([last_id] + data[1])
                        self.social_model.add_contact([last_id] + data[2])
                        self.detail_model.add_contact([last_id] + data[3])
                        self.info_model.add_contact([last_id] + data[4])
                        self.status_bar.set_count_text(self.mandatory_model.rowCount())
                    else:
                        ErrorHandler.database_error(self.mandatory_model.lastError().text(), False)
        except Exception as e:
            ErrorHandler.exception_handler(e)

    def delete_contact(self) -> None:
        try:
            index = self.table_view.selectionModel().currentIndex()
            if index.isValid():
                dialog = DeleteDialogs.show_delete_contact_dialog()
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    self.mandatory_model.delete_contact(index.row())
                    self.status_bar.set_count_text(self.mandatory_model.rowCount())
        except Exception as e:
            ErrorHandler.exception_handler(e)

    def delete_all_contacts(self) -> None:
        try:
            dialog = DeleteDialogs.show_delete_all_contacts_dialog()
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.mandatory_model.clear_database()
                self.status_bar.set_count_text(self.mandatory_model.rowCount())
        except Exception as e:
            ErrorHandler.exception_handler(e)