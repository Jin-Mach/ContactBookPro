from typing import Callable, TYPE_CHECKING

from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMainWindow

from src.contacts.threading.basic_thread import BasicThread
from src.contacts.threading.objects.check_birthday_object import CheckBirthdayObject
from src.contacts.ui.contacts_dialog.contacts_list_dialog import ContactsListDialog
from src.contacts.utilities.set_contact import show_selected_contact
from src.database.utilities.contacts_utilities.query_provider import QueryProvider
from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider

if TYPE_CHECKING:
    from src.database.models.mandatory_model import MandatoryModel
    from src.contacts.ui.main_widgets.contacts_tableview_widget import ContactsTableviewWidget
    from src.contacts.ui.main_widgets.contacts_statusbar_widget import ContactsStatusbarWidget


class CheckBirthdayController:
    def __init__(self, db_connection: QSqlDatabase, mandatory_model: "MandatoryModel", table_view: "ContactsTableviewWidget",
                 status_bar: "ContactsStatusbarWidget") -> None:
        self.class_name = "checkBirthdayController"
        self.db_connection = db_connection
        self.mandatory_model = mandatory_model
        self.table_view = table_view
        self.status_bar = status_bar

    def check_birthday(self, main_window: QMainWindow) -> None:
        try:
            query_provider = QueryProvider()
            birthday_object = CheckBirthdayObject(self.db_connection.databaseName(), query_provider, main_window)
            self.create_birthday_thread(birthday_object, birthday_object.run_check_birthday, main_window)
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)

    def create_birthday_thread(self, birthday_object: CheckBirthdayObject, start_slot: Callable[[], None],
                               main_window: QMainWindow) -> None:
        try:
            self.birthday_object = birthday_object
            self.birthday_thread = BasicThread()
            self.birthday_thread.run_basic_thread(worker=self.birthday_object, start_slot=start_slot,
                                                  on_error=lambda exception: ErrorHandler.write_log_exception(self.class_name, exception),
                                                  on_finished=lambda contacts_list: self.show_preview(main_window, contacts_list))
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)

    def show_preview(self, main_window: QMainWindow, contacts_list: list[dict[str, str]]) -> None:
        try:
            error_text = LanguageProvider.get_json_text("errors_text.json", self.class_name)
            if contacts_list is None:
                if error_text:
                    DialogsProvider.show_error_dialog(error_text.get("birthdayError", ""), main_window)
                return
            if contacts_list:
                order = ["id", "first_name", "second_name"]
                sorted_contacts_list = []
                for contact in contacts_list:
                    sorted_dict = {}
                    for key in order:
                        if key in contact:
                            sorted_dict[key] = contact[key]
                    sorted_contacts_list.append(sorted_dict)
                dialog = ContactsListDialog(sorted_contacts_list, "context_birthday", main_window, )
                if dialog.exec() == dialog.DialogCode.Rejected:
                    if dialog.result_code == "jump_to_contact" and dialog.selected_id:
                        show_selected_contact(self.mandatory_model, self.table_view, self.status_bar,
                                                dialog.selected_id)
            else:
                if error_text:
                    DialogsProvider.show_error_dialog(error_text.get("noBirthday", ""), main_window)
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)