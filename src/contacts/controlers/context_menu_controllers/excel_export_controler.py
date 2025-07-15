from typing import TYPE_CHECKING

from PyQt6.QtCore import QStandardPaths
from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMainWindow, QFileDialog

from src.contacts.threading.basic_thread import BasicThread
from src.contacts.threading.objects.export_excel_object import ExportExcelObject
from src.database.utilities.export_data_provider import ExportDataProvider
from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider
from src.utilities.logger_provider import get_logger

if TYPE_CHECKING:
    from src.contacts.ui.main_widgets.contacts_tableview_widget import ContactsTableviewWidget


class ExcelExportController:
    def __init__(self, db_connection: QSqlDatabase, table_view: "ContactsTableviewWidget") -> None:
        self.class_name = "excelExportController"
        self.export_path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
        self.db_connection = db_connection
        self.table_view = table_view
        self.export_data_provider = ExportDataProvider()
        self.menu_text = LanguageProvider.get_context_menu_text(self.class_name)
        self.error_text = LanguageProvider.get_error_text(self.class_name)

    def export_filtered_to_excel(self, main_window: QMainWindow) -> None:
        try:
            id_list = self.table_view.get_displayed_contacts_id()
            if not id_list:
                DialogsProvider.show_error_dialog(self.error_text.get("emptyIdList", ""), main_window)
                return
            file_name,_ = QFileDialog.getSaveFileName(parent=main_window, directory=self.export_path, filter=self.menu_text.get("excelFilter", ""))
            if file_name:
                export_object = ExportExcelObject(self.db_connection.databaseName(), file_name, id_list, self.export_data_provider, main_window)
                self.create_excel_thread(export_object, main_window)
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)

    def export_all_to_excel(self, main_window: QMainWindow) -> None:
        try:
            file_name, _ = QFileDialog.getSaveFileName(parent=main_window, directory=self.export_path, filter=self.menu_text.get("excelFilter", ""))
            if file_name:
                export_object = ExportExcelObject(self.db_connection.databaseName(), file_name, None, self.export_data_provider, main_window)
                self.create_excel_thread(export_object, main_window)
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)

    def create_excel_thread(self, export_object: ExportExcelObject, main_window: QMainWindow) -> None:
        try:
            self.excel_object = export_object
            self.excel_thread = BasicThread()
            self.excel_thread.run_basic_thread(worker=self.excel_object, start_slot=self.excel_object.run_excel_export,
                                               on_error=ExcelExportController.write_log_exception,
                                               on_finished=lambda success: ExcelExportController.notification_handler(
                                                 main_window, success))
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)

    @staticmethod
    def notification_handler(main_window: QMainWindow, success: bool) -> None:
        if success:
            main_window.tray_icon.show_notification("Export Excel", "exportSaved")
        else:
            main_window.tray_icon.show_notification("Export Excel", "saveError")

    @staticmethod
    def write_log_exception(exception: Exception) -> None:
        logger = get_logger()
        logger.error(exception, exc_info=True)