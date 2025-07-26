from typing import TYPE_CHECKING, Callable

from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMainWindow

from src.contacts.threading.basic_thread import BasicThread
from src.contacts.threading.objects.check_duplicates_object import CheckDuplicatesObject
from src.contacts.ui.contacts_dialog.contacts_list_dialog import ContactsListDialog
from src.contacts.utilities.set_contact import show_selected_contact
from src.database.utilities.contacts_utilities.query_provider import QueryProvider
from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider
from src.utilities.logger_provider import get_logger

if TYPE_CHECKING:
    from src.database.models.mandatory_model import MandatoryModel
    from src.contacts.ui.main_widgets.contacts_tableview_widget import ContactsTableviewWidget
    from src.contacts.ui.main_widgets.contacts_statusbar_widget import ContactsStatusbarWidget


class CheckDuplicatesController:
    def __init__(self, db_connection: QSqlDatabase, mandatory_model: "MandatoryModel", table_view: "ContactsTableviewWidget",
                 status_bar: "ContactsStatusbarWidget") -> None:
        self.class_name = "checkDuplicatesController"
        self.db_connection = db_connection
        self.mandatory_model = mandatory_model
        self.table_view = table_view
        self.status_bar = status_bar
        self.error_text = LanguageProvider.get_error_text(self.class_name)

    def check_duplicates(self, main_window: QMainWindow) -> None:
        try:
            query_provider = QueryProvider()
            duplicate_object = CheckDuplicatesObject(self.db_connection.databaseName(), query_provider, main_window)
            self.create_duplicate_thread(duplicate_object, duplicate_object.run_check_duplicates, main_window)
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)

    def create_duplicate_thread(self, duplicate_object: CheckDuplicatesObject, start_slot: Callable[[], None],
                                main_window: QMainWindow) -> None:
        try:
            self.duplicity_object = duplicate_object
            self.duplicity_thread = BasicThread()
            self.duplicity_thread.run_basic_thread(worker=self.duplicity_object, start_slot=start_slot,
                                                   on_error=CheckDuplicatesController.write_log_exception,
                                                   on_finished=lambda contacts_list: self.show_preview(main_window, contacts_list))
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
                dialog = ContactsListDialog(sorted_contacts_list, "context_duplicity", main_window, )
                if dialog.exec() == dialog.DialogCode.Rejected:
                    if dialog.result_code == "jump_to_contact" and dialog.selected_id:
                        show_selected_contact(self.mandatory_model, self.table_view, self.status_bar,
                                                dialog.selected_id)
            else:
                error_text = self.error_text.get("noDuplicates", "")
                DialogsProvider.show_error_dialog(error_text, main_window)
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)

    @staticmethod
    def write_log_exception(exception: Exception) -> None:
        logger = get_logger()
        logger.error(f"{CheckDuplicatesController.__class__.__name__}: {exception}", exc_info=True)