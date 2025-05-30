from datetime import datetime

from PyQt6.QtCore import QThreadPool, QModelIndex
from PyQt6.QtWidgets import QDialog, QMainWindow, QApplication

from src.contacts.contacts_ui.contacts_dialog.contact_dialog import ContactDialog
from src.contacts.contacts_ui.contacts_dialog.delete_dialogs import DeleteDialogs
from src.contacts.contacts_ui.widgets.contacts_detail_widget import ContactsDetailWidget
from src.contacts.contacts_ui.widgets.contacts_statusbar_widget import ContactsStatusbarWidget
from src.contacts.contacts_ui.widgets.contacts_tableview_widget import ContactsTableviewWidget
from src.contacts.contacts_utilities.get_main_window import get_main_window_instance
from src.database.database_utilities.models_refresher import refresh_models
from src.database.database_utilities.reset_database import reset_database
from src.database.database_utilities.row_data_provider import RowDataProvider
from src.database.database_utilities.update_models import update_models_data
from src.database.models.detail_model import DetailModel
from src.database.models.info_model import InfoModel
from src.database.models.mandatory_model import MandatoryModel
from src.database.models.social_model import SocialModel
from src.database.models.work_model import WorkModel
from src.threads.location_thread import LocationThread
from src.threads.signal_provider import SignalProvider
from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class ContactsController:
    def __init__(self, main_window: QMainWindow, mandatory_model: MandatoryModel, work_model: WorkModel, social_model: SocialModel, detail_model: DetailModel,
                 info_model: InfoModel, detail_widget: ContactsDetailWidget, table_view: ContactsTableviewWidget,
                 status_bar: ContactsStatusbarWidget, parent=None) -> None:
        self.main_window = main_window
        self.mandatory_model = mandatory_model
        self.work_model = work_model
        self.social_model = social_model
        self.detail_model = detail_model
        self.info_model = info_model
        self.detail_widget = detail_widget
        self.table_view = table_view
        self.status_bar = status_bar
        self.parent = parent
        self.signal_provider = SignalProvider()
        self.error_text = LanguageProvider.get_error_text("widgetErrors")
        self.table_view.doubleClicked.connect(self.update_contact)

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
                        self.status_bar.set_count_text(self.mandatory_model.rowCount(), self.status_bar.contacts_total_count + 1)
                        index = self.mandatory_model.index(self.mandatory_model.rowCount() - 1, 0)
                        self.table_view.selectRow(index.row())
                        self.table_view.scrollTo(index)
                        self.table_view.contact_data_controler.get_models_data(last_id)
                        self.main_window.tray_icon.show_notification(f"{data[0][2]} {data[0][3]}", "contactAdded")
                        location_thread = LocationThread(last_id, data[0], self.signal_provider)
                        QThreadPool.globalInstance().start(location_thread)
                        self.signal_provider.contact_coordinates.connect(lambda contact_id, coords: self.info_model.update_location_data(contact_id, coords))
                    else:
                        ErrorHandler.database_error(self.mandatory_model.lastError().text(), False, custom_message="queryError")
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def update_contact(self) -> None:
        try:
            if self.table_view.selectionModel().hasSelection():
                index = self.table_view.selectionModel().currentIndex()
                if index.isValid():
                    id_data = self.mandatory_model.index(index.row(), 0)
                    contact_id = self.mandatory_model.data(id_data)
                    contact_data = RowDataProvider.return_row_data(contact_id)
                    dialog = ContactDialog(True, contact_data, self.parent)
                    if dialog.exec() == dialog.DialogCode.Accepted:
                        new_data = dialog.colected_data
                        now = datetime.now().strftime("%d.%m.%Y")
                        models = [self.mandatory_model, self.work_model, self.social_model, self.detail_model, self.info_model]
                        if update_models_data(index.row(), contact_id, models, new_data, now, self.signal_provider):
                            self.table_view.set_detail_data(index)
                            self.main_window.tray_icon.show_notification(f"{contact_data["first_name"]} {contact_data["second_name"]}", "contactUpdated")
                else:
                    DialogsProvider.show_error_dialog(self.error_text["indexError"])
            else:
                DialogsProvider.show_error_dialog(self.error_text["noTableviewSelection"])
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def delete_contact(self) -> None:
        try:
            if self.table_view.selectionModel().hasSelection():
                index = self.table_view.currentIndex()
                if index.isValid():
                    dialog = DeleteDialogs.show_delete_contact_dialog()
                    if dialog.exec() == QDialog.DialogCode.Accepted:
                        self.mandatory_model.delete_contact(index.row())
                        refresh_models([self.mandatory_model, self.work_model, self.social_model, self.detail_model, self.info_model])
                        self.status_bar.set_count_text(self.mandatory_model.rowCount(), self.status_bar.contacts_total_count - 1)
                        self.detail_widget.reset_data()
                        self.main_window.tray_icon.show_notification("", "contactDeleted")
                else:
                    DialogsProvider.show_error_dialog(self.error_text["indexError"])
            else:
                DialogsProvider.show_error_dialog(self.error_text["noTableviewSelection"])
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def delete_all_contacts(self) -> None:
        try:
            dialog = DeleteDialogs.show_delete_all_contacts_dialog()
            if dialog.exec() == QDialog.DialogCode.Accepted:
                if not reset_database():
                    self.mandatory_model.clear_database()
                refresh_models([self.mandatory_model, self.work_model, self.social_model, self.detail_model, self.info_model])
                self.status_bar.set_count_text(self.mandatory_model.rowCount(), self.mandatory_model.rowCount())
                self.detail_widget.reset_data()
                self.main_window.tray_icon.show_notification("", "databaseDeleted")
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)