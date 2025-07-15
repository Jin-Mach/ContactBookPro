from typing import Callable

from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMainWindow

from src.contacts.threading.basic_thread import BasicThread
from src.contacts.threading.objects.check_birthday_object import CheckBirthdayObject
from src.database.utilities.query_provider import QueryProvider
from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider
from src.utilities.logger_provider import get_logger


class CheckBirthdayController:
    def __init__(self, db_connection: QSqlDatabase) -> None:
        self.class_name = "checkBirthdayController"
        self.db_connection = db_connection
        self.error_text = LanguageProvider.get_error_text(self.class_name)

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
                                                  on_error=CheckBirthdayController.write_log_exception,
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
                print(sorted_contacts_list)
            else:
                error_text = self.error_text.get("noBirthday", "")
                DialogsProvider.show_error_dialog(error_text, main_window)
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)

    @staticmethod
    def write_log_exception(exception: Exception) -> None:
        logger = get_logger()
        logger.error(exception, exc_info=True)