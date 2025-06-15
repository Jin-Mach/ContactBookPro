from PyQt6.QtCore import QStandardPaths, QObject, QThread
from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QTableView, QMainWindow, QFileDialog

from src.contacts.threading.export_excel_object import ExportExcelObject
from src.database.utilities.export_data_provider import ExportDataProvider
from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider
from src.utilities.logger_provider import get_logger


class ExcelExportControler:
    def __init__(self, db_connection: QSqlDatabase, table_view: QTableView) -> None:
        self.class_name = "excelExportControler"
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
                DialogsProvider.show_error_dialog(self.error_text["emptyIdList"], main_window)
                return
            headers, excel_data = ExportDataProvider.get_excel_data(self.db_connection, id_list, main_window)
            file_name,_ = QFileDialog.getSaveFileName(parent=main_window, directory=self.export_path, filter=self.menu_text["excelFilter"])
            if file_name:
                export_object = ExportExcelObject(file_name, headers, excel_data)
                self.create_excel_thread(export_object, main_window)
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)

    def export_all_to_excel(self, main_window: QMainWindow) -> None:
        try:
            headers, excel_data = ExportDataProvider.get_excel_data(self.db_connection, None, main_window)
            file_name, _ = QFileDialog.getSaveFileName(parent=main_window, directory=self.export_path, filter=self.menu_text["excelFilter"])
            if file_name:
                export_object = ExportExcelObject(file_name, headers, excel_data)
                self.create_excel_thread(export_object, main_window)
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)

    def create_excel_thread(self, export_object: QObject, main_window: QMainWindow) -> None:
        try:
            self.export_object = export_object
            self.export_thread = QThread()
            self.export_object.moveToThread(self.export_thread)
            self.export_thread.started.connect(self.export_object.run_excel_export)
            self.export_object.error_message.connect(ExcelExportControler.write_log_exception)
            self.export_object.finished.connect(self.export_thread.quit)
            self.export_object.finished.connect(self.export_object.deleteLater)
            self.export_thread.finished.connect(self.export_thread.deleteLater)
            self.export_object.finished.connect(lambda success: ExcelExportControler.notification_handler(main_window, success))
            self.export_thread.start()
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