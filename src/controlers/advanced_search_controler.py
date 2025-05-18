from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QDialog

from src.contacts.contacts_ui.search_dialog.advanced_search_dialog import AdvancedSearchDialog
from src.contacts.contacts_ui.widgets.contacts_statusbar_widget import ContactsStatusbarWidget
from src.database.database_utilities.search_provider import SearchProvider
from src.database.database_utilities.sql_query_creator import create_sql_query
from src.database.models.mandatory_model import MandatoryModel
from src.threads.advanced_search_thread import AdvancedSearchThread
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
        
    def advanced_search(self) -> None:
        try:
            dialog = AdvancedSearchDialog(self.parent)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                filters = dialog.get_finall_filter()
                query = create_sql_query(filters, self.parent)
                if query:
                    self.search_thread = AdvancedSearchThread(self.db_connection, query)
                    self.search_thread.search_completed.connect(self.check_search_result)
                    self.search_thread.error_message.connect(self.show_thread_error)
                    self.search_thread.start()
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def check_search_result(self, id_list: list) -> None:
        if not id_list:
            DialogsProvider.show_error_dialog(self.error_text["noFilteredData"])
            SearchProvider.reset_filter(self.mandatory_model)
            self.status_bar.set_count_text(self.mandatory_model.rowCount(), self.status_bar.contacts_total_count)
            return
        self.mandatory_model.set_advanced_search_filter(id_list)
        self.status_bar.set_count_text(self.mandatory_model.rowCount(), self.status_bar.contacts_total_count)

    @staticmethod
    def show_thread_error(error: str) -> None:
        ErrorHandler.database_error(error, False, custom_message="queryError")