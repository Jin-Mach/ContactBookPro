from typing import TYPE_CHECKING

from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMainWindow

from src.contacts.threading.basic_thread import BasicThread
from src.contacts.threading.objects.export_contacts_list_pdf_object import ExportContactsListPdfObject
from src.database.utilities.export_data_provider import ExportDataProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.logger_provider import get_logger

if TYPE_CHECKING:
    from src.contacts.ui.main_widgets.contacts_tableview_widget import ContactsTableviewWidget


class PdfExportController:

    def __init__(self, db_connection: QSqlDatabase, table_view: "ContactsTableviewWidget"):
        self.db_connection = db_connection
        self_table_view = table_view
        self.export_data_provider = ExportDataProvider()

    def export_all_list_to_pdf(self, main_window: QMainWindow) -> None:
        try:
            print("all list to pdf")
            export_object = ExportContactsListPdfObject(self.db_connection.databaseName(), None, self.export_data_provider,
                                                 main_window)
            self.create_pdf_thread(export_object, main_window)
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)

    def create_pdf_thread(self, export_object: ExportContactsListPdfObject, main_window: QMainWindow) -> None:
        try:
            self.pdf_object = export_object
            self.pdf_thread = BasicThread()
            self.pdf_thread.run_basic_thread(worker=self.pdf_object, start_slot=self.pdf_object.run_pdf_list_preview,
                                             on_error=PdfExportController.write_log_exception,
                                             on_finished=lambda success, file_path: PdfExportController.show_preview(main_window, success, file_path))
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)

    @staticmethod
    def show_preview(main_window: QMainWindow, success: bool, file_path: str) -> None:
        if success:
            print("náhled ok, cesta:", file_path)
        else:
            print("náhled nevyšel")

    @staticmethod
    def write_log_exception(exception: Exception) -> None:
        logger = get_logger()
        logger.error(exception, exc_info=True)