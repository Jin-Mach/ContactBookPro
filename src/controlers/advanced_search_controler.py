from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QDialog

from src.contacts.contacts_ui.search_dialog.advanced_search_dialog import AdvancedSearchDialog
from src.database.database_utilities.sql_query_creator import create_sql_query
from src.utilities.error_handler import ErrorHandler


class AdvancedSearchControler:
    def __init__(self, db_connection: QSqlDatabase, parent=None) -> None:
        self.db_connection= db_connection
        self.parent = parent
        
    def advanced_search(self) -> None:
        try:
            dialog = AdvancedSearchDialog(self.parent)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                filters = dialog.get_finall_filter()
                query = create_sql_query(filters, self.parent)
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)