import pathlib
import shutil

from typing import TYPE_CHECKING, Callable

from PyQt6.QtCore import QStandardPaths
from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMainWindow, QFileDialog

from src.contacts.threading.basic_thread import BasicThread
from src.contacts.threading.objects.export_contacts_list_pdf_object import ExportContactsListPdfObject
from src.contacts.threading.objects.export_contact_pdf_object import ExportContactPdfObject
from src.contacts.ui.preview_widgets.pdf_preview import PdfPreviewDialog
from src.database.utilities.contacts_utilities.export_data_provider import ExportDataProvider
from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider
from src.utilities.logger_provider import get_logger

if TYPE_CHECKING:
    from src.contacts.ui.main_widgets.contacts_tableview_widget import ContactsTableviewWidget


# noinspection PyBroadException
class PdfExportController:

    def __init__(self, db_connection: QSqlDatabase, table_view: "ContactsTableviewWidget"):
        self.class_name = "pdfExportController"
        self.db_connection = db_connection
        self.table_view = table_view
        self.export_data_provider = ExportDataProvider()
        self.error_text = LanguageProvider.get_error_text(self.class_name)
        self.pdf_output_path = pathlib.Path(__file__).parents[4].joinpath("output", "pdf_output.pdf")
        self.pdf_output_path.parent.mkdir(parents=True, exist_ok=True)

    def export_contact_to_pdf(self, main_window:QMainWindow) -> None:
        try:
            if not self.table_view.selectionModel().hasSelection():
                DialogsProvider.show_error_dialog(self.error_text.get("noTableviewSelection", ""), main_window)
                return
            index = self.table_view.selectionModel().currentIndex()
            if not index.isValid():
                DialogsProvider.show_error_dialog(self.error_text.get("indexError", ""), main_window)
                return
            mandatory_model = self.table_view.mandatory_model
            id_data = mandatory_model.index(index.row(), 0)
            contact_id = mandatory_model.data(id_data)
            export_object = ExportContactPdfObject(self.db_connection.databaseName(), self.pdf_output_path,
                                                   contact_id, self.export_data_provider, main_window)
            self.create_pdf_thread(export_object, export_object.run_pdf_contact_export, main_window)
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)

    def export_filtered_list_to_pdf(self, main_window: QMainWindow) -> None:
        try:
            id_list = self.table_view.get_displayed_contacts_id()
            if not id_list:
                DialogsProvider.show_error_dialog(self.error_text.get("emptyIdList", ""), main_window)
                return
            export_object = ExportContactsListPdfObject(self.db_connection.databaseName(), self.pdf_output_path,
                                                        id_list, self.export_data_provider, main_window)
            self.create_pdf_thread(export_object,export_object.run_pdf_list_export,  main_window)
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)

    def export_all_list_to_pdf(self, main_window: QMainWindow) -> None:
        try:
            export_object = ExportContactsListPdfObject(self.db_connection.databaseName(), self.pdf_output_path,
                                                        None, self.export_data_provider, main_window)
            self.create_pdf_thread(export_object, export_object.run_pdf_list_export, main_window)
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)

    def create_pdf_thread(self, export_object: ExportContactsListPdfObject | ExportContactPdfObject, start_slot: Callable[[], None],
                          main_window: QMainWindow) -> None:
        try:
            self.pdf_object = export_object
            self.pdf_thread = BasicThread()
            self.pdf_thread.run_basic_thread(worker=self.pdf_object, start_slot=start_slot,
                                             on_error=PdfExportController.write_log_exception,
                                             on_finished=lambda success: self.show_preview(main_window, success))
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)

    def show_preview(self, main_window: QMainWindow, success: bool) -> None:
        try:
            if success:
                pdf_dialog = PdfPreviewDialog(str(self.pdf_output_path), lambda: self.save_pdf_document(str(self.pdf_output_path), main_window), main_window)
                pdf_dialog.exec()
            else:
                main_window.tray_icon.show_notification("Export PDF", "saveError")
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)

    def save_pdf_document(self, default_file_path: str, main_window:QMainWindow) -> None:
        try:
            default_path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
            menu_text = LanguageProvider.get_context_menu_text(self.class_name)
            file, _ = QFileDialog.getSaveFileName(parent=main_window, directory=default_path, filter=menu_text.get("pdfFilter", ""))
            if not file:
                return
            try:
                shutil.copyfile(default_file_path, str(file))
                main_window.tray_icon.show_notification("Export PDF", "exportSaved")
            except Exception:
                main_window.tray_icon.show_notification("Export PDF", "saveError")
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)

    @staticmethod
    def write_log_exception(exception: Exception) -> None:
        logger = get_logger()
        logger.error(exception, exc_info=True)