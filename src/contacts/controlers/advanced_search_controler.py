from PyQt6.QtCore import QThread
from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QDialog

from src.contacts.threading.advanced_search_object import AdvancedSearchObject
from src.contacts.threading.user_filter_object import UserFilterObject
from src.contacts.ui.search_dialogs.advanced_search_dialog import AdvancedSearchDialog
from src.contacts.ui.widgets.contacts_statusbar_widget import ContactsStatusbarWidget
from src.database.models.mandatory_model import MandatoryModel
from src.database.utilities.query_provider import QueryProvider
from src.database.utilities.search_provider import SearchProvider
from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider
from src.utilities.logger_provider import get_logger


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
                query = QueryProvider.create_search_query(filters, self.parent)
                if query:
                    self.advanced_search_object = AdvancedSearchObject(self.db_connection.databaseName(), query)
                    self.advanced_search_thread = QThread()
                    self.advanced_search_object.moveToThread(self.advanced_search_thread)
                    self.advanced_search_thread.started.connect(self.advanced_search_object.run_advanced_search)
                    self.advanced_search_object.search_completed.connect(self.check_search_result)
                    self.advanced_search_object.error_message.connect(self.log_and_show_error)
                    self.advanced_search_object.finished.connect(self.advanced_search_thread.quit)
                    self.advanced_search_thread.finished.connect(self.advanced_search_object.deleteLater)
                    self.advanced_search_thread.finished.connect(self.advanced_search_thread.deleteLater)
                    self.advanced_search_object.finished.connect(lambda: AdvancedSearchControler.remove_connection(self.advanced_search_object.connection_name))
                    self.advanced_search_thread.start()
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def apply_saved_filter(self, selected_filter: dict) -> None:
        try:
            query = QueryProvider.create_search_query(selected_filter, self.parent)
            if query:
                self.user_filter_object = UserFilterObject(self.db_connection.databaseName(), query)
                self.user_filter_thread = QThread()
                self.user_filter_object.moveToThread(self.user_filter_thread)
                self.user_filter_thread.started.connect(self.user_filter_object.run_user_filter)
                self.user_filter_object.search_completed.connect(self.check_search_result)
                self.user_filter_object.error_message.connect(self.log_and_show_error)
                self.user_filter_object.finished.connect(self.user_filter_thread.quit)
                self.user_filter_thread.finished.connect(self.user_filter_object.deleteLater)
                self.user_filter_thread.finished.connect(self.user_filter_thread.deleteLater)
                self.user_filter_object.finished.connect(lambda: AdvancedSearchControler.remove_connection(self.user_filter_object.connection_name))
                self.user_filter_thread.start()
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
    def log_and_show_error(error: str) -> None:
        logger = get_logger()
        logger.error(error, exc_info=True)
        ErrorHandler.database_error(error, False, custom_message="queryError")