from typing import TYPE_CHECKING, Callable

from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMainWindow

from src.contacts.threading.basic_thread import BasicThread
from src.contacts.threading.objects.check_coords_object import CheckCoordsObject
from src.contacts.ui.contacts_dialog.contacts_list_dialog import ContactsListDialog
from src.contacts.utilities.set_contact import show_selected_contact
from src.database.utilities.contacts_utilities.query_provider import QueryProvider
from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider
from src.utilities.logger_provider import get_logger

if TYPE_CHECKING:
    from src.contacts.ui.main_widgets.contacts_tableview_widget import ContactsTableviewWidget
    from src.database.models.mandatory_model import MandatoryModel
    from src.contacts.ui.main_widgets.contacts_statusbar_widget import ContactsStatusbarWidget


class CheckCoordinatesController:
    def __init__(self, db_connection: QSqlDatabase, mandatory_model: "MandatoryModel", table_view: "ContactsTableviewWidget",
                 status_bar: "ContactsStatusbarWidget") -> None:
        self.class_name = "checkCoordinatesController"
        self.db_connection = db_connection
        self.mandatory_model = mandatory_model
        self.table_view = table_view
        self.status_bar = status_bar

    def check_coords(self, main_window: QMainWindow) -> None:
        try:
            query_provider = QueryProvider()
            coords_object = CheckCoordsObject(self.db_connection.databaseName(), query_provider, main_window)
            self.create_coords_thread(coords_object, coords_object.run_check_coords, main_window)
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)

    def create_coords_thread(self, coords_object: CheckCoordsObject, start_slot: Callable[[], None],
                             main_window: QMainWindow) -> None:
        try:
            self.coords_object = coords_object
            self.coords_thread = BasicThread()
            self.coords_thread.run_basic_thread(worker=self.coords_object, start_slot=start_slot,
                                                on_error=CheckCoordinatesController.write_log_exception,
                                                on_finished=lambda contact_list: self.show_preview(main_window, contact_list))
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)

    def show_preview(self, main_window: QMainWindow, contacts_list: list[dict[str, str]]) -> None:
        try:
            if contacts_list:
                order = ["id", "first_name", "second_name"]
                sorted_contacts_list = []
                for contact in contacts_list:
                    sorted_dict = {}
                    for key in order:
                        if key in contact:
                            sorted_dict[key] = contact[key]
                    sorted_contacts_list.append(sorted_dict)
                dialog = ContactsListDialog(sorted_contacts_list, "context_coordinates", main_window, )
                if dialog.exec() == dialog.DialogCode.Rejected:
                    if dialog.result_code == "jump_to_contact" and dialog.selected_id:
                        show_selected_contact(self.mandatory_model, self.table_view, self.status_bar,
                                                dialog.selected_id)
            else:
                error_text = LanguageProvider.get_json_text("errors_text.json", self.class_name)
                if error_text:
                    error_text = error_text.get("noCoordinates", "")
                    DialogsProvider.show_error_dialog(error_text, main_window)
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)

    @staticmethod
    def write_log_exception(exception: Exception) -> None:
        logger = get_logger()
        logger.error(f"{CheckCoordinatesController.__class__.__name__}: {exception}", exc_info=True)