from typing import TYPE_CHECKING

from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QDialog

from src.contacts.threading.basic_thread import BasicThread
from src.contacts.threading.objects.advanced_search_object import AdvancedSearchObject
from src.contacts.threading.objects.user_filter_object import UserFilterObject
from src.contacts.ui.search_dialogs.advanced_search_dialog import AdvancedSearchDialog
from src.contacts.ui.shared_widgets.progress_dialog import ProgressDialog
from src.database.utilities.contacts_utilities.query_provider import QueryProvider
from src.database.utilities.contacts_utilities.search_provider import SearchProvider
from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider
from src.utilities.logger_provider import get_logger

if TYPE_CHECKING:
    from src.database.models.mandatory_model import MandatoryModel
    from src.contacts.ui.main_widgets.contacts_statusbar_widget import ContactsStatusbarWidget


class AdvancedSearchController:
    def __init__(self, db_connection: QSqlDatabase, mandatory_model: "MandatoryModel", contacts_statusbar: "ContactsStatusbarWidget",
                 parent=None) -> None:
        self.db_connection= db_connection
        self.mandatory_model = mandatory_model
        self.contacts_statusbar = contacts_statusbar
        self.error_text = LanguageProvider.get_error_text("contactSearchController")
        self.parent = parent
        self.dialog = AdvancedSearchDialog(self.parent)
        self.query_provider = QueryProvider()
        self.progress_dialog = ProgressDialog(self.parent)

    def advanced_search(self) -> None:
        try:
            self.dialog.reset_all_filters()
            if self.dialog.exec() == QDialog.DialogCode.Accepted:
                self.progress_dialog.show_dialog()
                filters = self.dialog.get_final_filter()
                self.advanced_search_object = AdvancedSearchObject(self.db_connection.databaseName(), self.query_provider, filters, self.parent)
                self.advanced_search_thread = BasicThread()
                self.advanced_search_thread.run_basic_thread(worker=self.advanced_search_object,
                                                             start_slot=self.advanced_search_object.run_advanced_search,
                                                             success_signal=self.advanced_search_object.search_completed,
                                                             success_callback=self.check_search_result,
                                                             on_error=self.log_and_show_error,
                                                             on_finished=lambda: self.search_finished(self.advanced_search_object.connection_name))
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def apply_saved_filter(self, selected_filter: dict) -> None:
        try:
            self.progress_dialog.show_dialog()
            self.user_filter_object = UserFilterObject(self.db_connection.databaseName(), self.query_provider, selected_filter, self.parent)
            self.user_filter_thread = BasicThread()
            self.user_filter_thread.run_basic_thread(worker=self.user_filter_object,
                                                     start_slot=self.user_filter_object.run_user_filter,
                                                     success_signal=self.user_filter_object.search_completed,
                                                     success_callback=self.check_search_result,
                                                     on_error=self.log_and_show_error,
                                                     on_finished=lambda: self.search_finished(self.user_filter_object.connection_name))
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def check_search_result(self, id_list: list) -> None:
        try:
            if not id_list:
                self.progress_dialog.hide_dialog()
                DialogsProvider.show_error_dialog(self.error_text.get("noFilteredData", ""), self.parent)
                SearchProvider.reset_filter(self.mandatory_model)
                self.contacts_statusbar.set_count_text(self.mandatory_model.rowCount(), 0)
                return
            self.mandatory_model.set_filter_by_id(id_list)
            self.contacts_statusbar.set_count_text(self.mandatory_model.rowCount(), 0)
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def search_finished(self, connection_name: str) -> None:
        try:
            QSqlDatabase.removeDatabase(connection_name)
        except Exception as e:
            logger = get_logger()
            logger.error(f"{self.__class__.__name__}: {e}", exc_info=True)
        finally:
            if self.progress_dialog and self.progress_dialog.isVisible():
                self.progress_dialog.hide_dialog()

    @staticmethod
    def log_and_show_error(error: str) -> None:
        print(error)
        logger = get_logger()
        logger.error(f"{AdvancedSearchController.__class__.__name__}: {error}", exc_info=True)
        ErrorHandler.database_error(error, False, custom_message="queryError")