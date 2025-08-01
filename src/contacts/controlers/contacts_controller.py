from datetime import datetime
from typing import Any, TYPE_CHECKING

from PyQt6.QtCore import QThreadPool, QModelIndex, QThread, QTimer
from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QDialog, QMainWindow, QCheckBox

from src.contacts.threading.location_thread import LocationThread
from src.contacts.threading.objects.update_locations_object import UpdateLocationsObject
from src.contacts.threading.signal_provider import SignalProvider
from src.contacts.ui.contacts_dialog.contact_dialog import ContactDialog
from src.contacts.ui.contacts_dialog.delete_dialogs import DeleteDialogs
from src.contacts.ui.contacts_dialog.contacts_list_dialog import ContactsListDialog
from src.contacts.utilities.check_update_data import CheckUpdateProvider
from src.contacts.utilities.filters_provider import FiltersProvider
from src.contacts.utilities.set_contact import show_selected_contact
from src.database.utilities.contacts_utilities.models_refresher import refresh_models
from src.database.utilities.contacts_utilities.query_provider import QueryProvider
from src.database.utilities.contacts_utilities.reset_database import reset_database
from src.database.utilities.contacts_utilities.row_data_provider import RowDataProvider
from src.database.utilities.contacts_utilities.update_models import update_models_data
from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider
from src.utilities.application_support_provider import ApplicationSupportProvider

if TYPE_CHECKING:
    from src.database.models.mandatory_model import MandatoryModel
    from src.database.models.work_model import WorkModel
    from src.database.models.social_model import SocialModel
    from src.database.models.detail_model import DetailModel
    from src.database.models.info_model import InfoModel
    from src.contacts.ui.main_widgets.contacts_detail_widget import ContactsDetailWidget
    from src.contacts.ui.main_widgets.contacts_tableview_widget import ContactsTableviewWidget
    from src.contacts.ui.main_widgets.contacts_statusbar_widget import ContactsStatusbarWidget
    from src.map.controllers.map_controller import MapController
    from src.statistics.controllers.statistics_controller import StatisticsController


# noinspection PyUnresolvedReferences
class ContactsController:
    def __init__(self, main_window: QMainWindow, db_connection: QSqlDatabase, mandatory_model: "MandatoryModel",
                 work_model: "WorkModel", social_model: "SocialModel", detail_model: "DetailModel", info_model: "InfoModel",
                 detail_widget: "ContactsDetailWidget", table_view: "ContactsTableviewWidget", contacts_statusbar: "ContactsStatusbarWidget",
                 map_controller: "MapController", statistics_controller: "StatisticsController", parent=None) -> None:
        self.main_window = main_window
        self.db_connection = db_connection
        self.mandatory_model = mandatory_model
        self.work_model = work_model
        self.social_model = social_model
        self.detail_model = detail_model
        self.info_model = info_model
        self.detail_widget = detail_widget
        self.table_view = table_view
        self.contacts_statusbar = contacts_statusbar
        self.map_controller = map_controller
        self.statistics_controller = statistics_controller
        self.parent = parent
        self.signal_provider = SignalProvider()
        self.error_text = LanguageProvider.get_error_text("widgetErrors")
        self.table_view.doubleClicked.connect(self.update_contact)
        self.signal_provider.contact_coordinates.connect(self.on_location_updated)
        QTimer.singleShot(5 * 60 * 1000, self.update_locations)

    def on_location_updated(self, contact_id: int, coords: tuple[float, float]) -> None:
        self.info_model.update_location_data(contact_id, coords)
        self.map_controller.create_map()
        self.statistics_controller.set_data()

    def get_selected_contact_data(self) -> tuple[QModelIndex, int, dict[str, Any]] | None:
        if not self.table_view.selectionModel().hasSelection():
            DialogsProvider.show_error_dialog(self.error_text.get("noTableviewSelection", ""), self.parent)
            return None
        index = self.table_view.selectionModel().currentIndex()
        if not index.isValid():
            DialogsProvider.show_error_dialog(self.error_text.get("indexError", ""), self.parent)
            return None
        id_data = self.mandatory_model.index(index.row(), 0)
        contact_id = self.mandatory_model.data(id_data)
        contact_data = RowDataProvider.return_row_data(self.db_connection, contact_id)
        return index, contact_id, contact_data

    def refresh_ui(self, added: int | None) -> None:
        refresh_models([
            self.mandatory_model, self.work_model, self.social_model,
            self.detail_model, self.info_model
        ])
        if added is None:
            self.contacts_statusbar.set_count_text(self.mandatory_model.rowCount(), None)
        else:
            self.contacts_statusbar.set_count_text(self.mandatory_model.rowCount(), added)
        self.detail_widget.reset_data()

    def check_duplicates(self, contact_id: int | None, first_name: str, last_name: str) -> bool:
        duplicity = QueryProvider.create_check_duplicate_query(self.db_connection, contact_id, first_name, last_name)
        if duplicity:
            dialog = ContactsListDialog(duplicity, "validation", self.parent)
            if dialog.exec() == QDialog.DialogCode.Rejected:
                if dialog.result_code == "rejected":
                    return False
                elif dialog.result_code == "jump_to_contact" and dialog.selected_id:
                    show_selected_contact(self.mandatory_model, self.table_view, self.contacts_statusbar,
                                          dialog.selected_id)
                return False
        return True

    def add_new_contact(self) -> None:
        try:
            dialog = ContactDialog(False, self.parent)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.colected_data
                if data:
                    mandatory_data = data[0]
                    if not self.check_duplicates(None, mandatory_data[4], mandatory_data[5]):
                        return
                    self.mandatory_model.add_contact(mandatory_data)
                    last_id = RowDataProvider.get_last_id(self.mandatory_model)
                    if last_id != -1:
                        self.work_model.add_contact([last_id] + data[1])
                        self.social_model.add_contact([last_id] + data[2])
                        self.detail_model.add_contact([last_id] + data[3])
                        self.info_model.add_contact([last_id] + data[4])
                        self.refresh_ui(1)
                        index = self.mandatory_model.index(self.mandatory_model.rowCount() - 1, 0)
                        self.table_view.selectRow(index.row())
                        self.table_view.scrollTo(index)
                        self.table_view.contact_data_controller.get_models_data(last_id)
                        self.main_window.tray_icon.show_notification(f"{data[0][2]} {data[0][3]}", "contactAdded")
                        QThreadPool.globalInstance().start(LocationThread(last_id, data[0], self.signal_provider))
                    else:
                        ErrorHandler.database_error(self.mandatory_model.lastError().text(), False, custom_message="queryError")
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def update_contact(self) -> None:
        try:
            selected_contact = self.get_selected_contact_data()
            if selected_contact is None:
                return
            index, contact_id, contact_data = selected_contact
            dialog = ContactDialog(True, contact_data, self.parent)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                new_data = dialog.colected_data
                if not new_data:
                    return
                if CheckUpdateProvider.check_data_changed(new_data):
                    return
                mandatory_data = new_data[0][0]
                if not self.check_duplicates(contact_id, mandatory_data[4], mandatory_data[5]):
                    return
                now = datetime.now().strftime("%d.%m.%Y")
                models = [
                    self.mandatory_model, self.work_model, self.social_model,
                    self.detail_model, self.info_model
                ]
                if update_models_data(index.row(), contact_id, models, new_data, now, self.signal_provider, self.map_controller):
                    self.table_view.set_detail_data(index)
                    self.table_view.select_contact_by_id(contact_id)
                    self.main_window.tray_icon.show_notification(
                        f'{new_data[0][0][2]} {new_data[0][0][3]}',
                        "contactUpdated"
                    )
                self.statistics_controller.set_data()
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def delete_contact(self) -> None:
        try:
            selected_contact = self.get_selected_contact_data()
            if selected_contact is None:
                return
            index, contact_id, contact_data = selected_contact
            dialog = DeleteDialogs.show_delete_contact_dialog(contact_data.get("first_name", ""), contact_data.get("second_name", ""))
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.mandatory_model.delete_contact(index.row())
                self.refresh_ui(-1)
                self.main_window.tray_icon.show_notification("", "contactDeleted")
                self.map_controller.create_map()
                self.statistics_controller.set_data()
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def delete_all_contacts(self) -> None:
        try:
            dialog = DeleteDialogs.show_delete_all_contacts_dialog()
            check_box = dialog.findChild(QCheckBox, "deleteFiltersCheckbox")
            if dialog.exec() == QDialog.DialogCode.Accepted:
                if isinstance(check_box, QCheckBox) and check_box.isChecked():
                    FiltersProvider.delete_filters_file()
                self.mandatory_model.clear_database()
                if not reset_database():
                    self.refresh_ui(None)
                self.main_window.tray_icon.show_notification("", "databaseDeleted")
                self.map_controller.create_map()
                self.statistics_controller.set_data()
                try:
                    ApplicationSupportProvider.restart_application()
                except Exception:
                    ErrorHandler.exception_handler(OSError())
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def update_locations(self) -> None:
        try:
            self.location_object = UpdateLocationsObject(self.db_connection.databaseName(), self.main_window)
            self.location_thread = QThread()
            self.location_object.moveToThread(self.location_thread)
            self.location_thread.started.connect(self.location_object.get_locations)
            self.location_object.finished.connect(self.update_coordinates)
            self.location_object.finished.connect(self.location_thread.quit)
            self.location_object.finished.connect(self.location_object.deleteLater)
            self.location_thread.finished.connect(self.location_thread.deleteLater)
            self.location_thread.start()
        except Exception as e:
            ErrorHandler.exception_handler(e, self.main_window)

    def update_coordinates(self, data: list[tuple[int, tuple[float, float]]]) -> None:
        try:
            if data:
                for contact in data:
                    self.info_model.update_location_data(contact[0], contact[1])
                self.statistics_controller.set_data()
                self.map_controller.create_map()
        except Exception as e:
            ErrorHandler.exception_handler(e, self.main_window)