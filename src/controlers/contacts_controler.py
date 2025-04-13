from PyQt6.QtWidgets import QDialog

from src.contacts.contacts_ui.dialogs.contact_dialog import ContactDialog
from src.contacts.contacts_ui.dialogs.delete_dialogs import DeleteDialogs
from src.contacts.contacts_ui.widgets.contacts_tableview_widget import ContactsTableviewWidget
from src.database.models.mandatory_model import MandatoryModel
from src.utilities.error_handler import ErrorHandler


class ContactsControler:
    def __init__(self, mandatory_model: MandatoryModel, table_view: ContactsTableviewWidget) -> None:
        self.mandatory_model = mandatory_model
        self.table_view = table_view

    def add_new_contact(self) -> None:
        try:
            dialog = ContactDialog()
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.new_data()
                if data:
                    self.mandatory_model.add_contact(data[0])
        except Exception as e:
            ErrorHandler.exception_handler(e)

    def delete_contact(self) -> None:
        try:
            index = self.table_view.selectionModel().currentIndex()
            if index.isValid():
                dialog = DeleteDialogs.show_delete_contact_dialog()
                if dialog.exec() == QDialog.DialogCode.Accepted:
                        self.mandatory_model.delete_contact(index.row())
        except Exception as e:
            ErrorHandler.exception_handler(e)

    def delete_all_contacts(self) -> None:
        try:
            dialog = DeleteDialogs.show_delete_all_contacts_dialog()
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.mandatory_model.clear_database()
        except Exception as e:
            ErrorHandler.exception_handler(e)