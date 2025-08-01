from PyQt6.QtCore import QStandardPaths
from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMainWindow, QFileDialog

from src.contacts.utilities.generate_vcard import create_vcard
from src.database.utilities.contacts_utilities.row_data_provider import RowDataProvider
from src.utilities.application_support_provider import ApplicationSupportProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


# noinspection PyUnresolvedReferences
def export_to_vcard(db_connection: QSqlDatabase, index: int, main_window: QMainWindow) -> None:
    try:
        menu_text = LanguageProvider.get_context_menu_text("vcardExportController")
        contact_row_data = RowDataProvider.return_row_data(db_connection, index)
        if not contact_row_data:
            return
        file_name,_ = QFileDialog.getSaveFileName(parent=main_window, directory=QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation),
                                                  filter=menu_text.get("vcardFilter", ""))
        if file_name:
            with open(file_name, "w", encoding=ApplicationSupportProvider.get_encoding()) as file:
                file.write(create_vcard(contact_row_data, main_window=main_window))
                main_window.tray_icon.show_notification("Export vCard", "exportSaved")
    except Exception as e:
        ErrorHandler.exception_handler(e, main_window)