from typing import TYPE_CHECKING

from PyQt6.QtSql import QSqlDatabase

from src.database.utilities.row_data_provider import RowDataProvider
from src.utilities.error_handler import ErrorHandler

if TYPE_CHECKING:
    from src.contacts.ui.main_widgets.contacts_detail_widget import ContactsDetailWidget


class ContactDataController:
    def __init__(self, db_connection: QSqlDatabase, detail_widget: "ContactsDetailWidget") -> None:
        self.db_connection = db_connection
        self.contacts_detail_widget = detail_widget

    def get_models_data(self, index: int, parent=None) -> None:
        try:
            data = RowDataProvider.return_row_data(self.db_connection, index) or {}
            self.contacts_detail_widget.personal_info_widget.set_data(data)
            self.contacts_detail_widget.tab_info_widget.set_data(data)
            self.contacts_detail_widget.notes_info_widget.set_data(data)
        except Exception as e:
            ErrorHandler.exception_handler(e, parent)