from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QDialog

from src.contacts.contacts_ui.search_dialog.advanced_search_dialog import AdvancedSearchDialog
from src.contacts.contacts_ui.widgets.contacts_statusbar_widget import ContactsStatusbarWidget
from src.database.database_utilities.search_provider import SearchProvider
from src.database.database_utilities.sql_query_creator import create_search_query
from src.database.models.mandatory_model import MandatoryModel
from src.threads.advanced_search_thread import AdvancedSearchThread
from src.threads.user_filter_thread import UserFilterThread
from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class AdvancedSearchControler:
    def __init__(self, db_connection: QSqlDatabase, mandatory_model: MandatoryModel, status_bar: ContactsStatusbarWidget,
                 parent=None) -> None:
        self.db_connection= db_connection
        self.mandatory_model = mandatory_model
        self.status_bar = status_bar
        self.error_text = LanguageProvider.get_error_text("contactSearchControler")
        self.parent = parent
        self.dialog = AdvancedSearchDialog(self.parent)
        
    def advanced_search(self) -> None:
        try:
            self.dialog.reset_all_filters()
            if self.dialog.exec() == QDialog.DialogCode.Accepted:
                filters = self.dialog.get_finall_filter()
                query = create_search_query(filters, self.parent)
                if query:
                    advanced_search_thread = AdvancedSearchThread(self.db_connection.databaseName(), query)
                    advanced_search_thread.search_completed.connect(self.check_search_result)
                    advanced_search_thread.error_message.connect(self.show_thread_error)
                    advanced_search_thread.finished.connect(lambda: self.remove_connection(advanced_search_thread.connection_name))
                    advanced_search_thread.start()
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def apply_saved_filter(self, selected_filter: dict) -> None:
        try:
            query = create_search_query(selected_filter, self.parent)
            if query:
                user_filter_thread = UserFilterThread(self.db_connection.databaseName(), query)
                user_filter_thread.search_completed.connect(self.check_search_result)
                user_filter_thread.error_message.connect(self.show_thread_error)
                user_filter_thread.finished.connect(lambda: self.remove_connection(user_filter_thread.connection_name))
                user_filter_thread.start()
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def check_search_result(self, id_list: list) -> None:
        if not id_list:
            DialogsProvider.show_error_dialog(self.error_text["noFilteredData"])
            SearchProvider.reset_filter(self.mandatory_model)
            self.status_bar.set_count_text(self.mandatory_model.rowCount(), 0)
            return
        self.mandatory_model.set_filter_by_id(id_list)
        self.status_bar.set_count_text(self.mandatory_model.rowCount(), 0)

    @staticmethod
    def remove_connection(connection_name: str)-> None:
        QSqlDatabase.removeDatabase(connection_name)

    @staticmethod
    def show_thread_error(error: str) -> None:
        ErrorHandler.database_error(error, False, custom_message="queryError")