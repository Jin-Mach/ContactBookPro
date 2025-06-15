from PyQt6.QtCore import QStandardPaths, QThread
from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableView, QFileDialog

from src.contacts.threading.export_cvs_object import ExportCsvObject
from src.database.utilities.export_data_provider import ExportDataProvider
from src.database.utilities.row_data_provider import RowDataProvider
from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider
from src.utilities.logger_provider import get_logger


class ExportControler:
    def __init__(self, db_connection: QSqlDatabase, table_view: QTableView) -> None:
        self.class_name = "exportControler"
        self.export_path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
        self.db_connection = db_connection
        self.table_view = table_view
        self.export_data_provider = ExportDataProvider()
        self.menu_text = LanguageProvider.get_context_menu_text(self.class_name)
        self.error_text = LanguageProvider.get_error_text(self.class_name)

    def copy_to_clipboard(self, index: int, field: str, main_window: QMainWindow) -> None:
        try:
            clipboard = QApplication.clipboard()
            row_data = RowDataProvider.return_row_data(self.db_connection, index)
            title_text = f"{row_data['first_name']} {row_data['second_name']}"
            if field == "name":
                clipboard.setText(f"{row_data['first_name']} {row_data['second_name']}")
            elif field == "email":
                clipboard.setText(row_data["personal_email"])
            elif field == "phone":
                clipboard.setText(row_data["personal_phone_number"])
            main_window.tray_icon.show_notification(title_text, f"{field}Copied")
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)

    def export_to_csv(self, main_window: QMainWindow) -> None:
        try:
            id_list = self.table_view.get_displayed_contacts_id()
            if not id_list:
                DialogsProvider.show_error_dialog(self.error_text["emptyIdList"], main_window)
                return
            semicolon, headers, csv_data = self.export_data_provider.get_filtered_data_csv(self.db_connection, id_list, self.table_view)
            delimiter = ","
            if semicolon:
                delimiter = ";"
            file_name,_ = QFileDialog.getSaveFileName(parent=main_window, directory=self.export_path, filter=self.menu_text["csvFilter"])
            if file_name:
                self.export_filtered_object = ExportCsvObject(file_name, headers, delimiter, csv_data)
                self.export_filtered_thread = QThread()
                self.export_filtered_object.moveToThread(self.export_filtered_thread)
                self.export_filtered_thread.started.connect(self.export_filtered_object.run_filtered_export)
                self.export_filtered_object.filtered_error_message.connect(ExportControler.write_log_exception)
                self.export_filtered_object.filtered_finished.connect(self.export_filtered_thread.quit)
                self.export_filtered_object.filtered_finished.connect(self.export_filtered_object.deleteLater)
                self.export_filtered_thread.finished.connect(self.export_filtered_thread.deleteLater)
                self.export_filtered_object.filtered_finished.connect(lambda success: ExportControler.notification_handler(main_window, success))
                self.export_filtered_thread.start()
        except Exception as e:
            ErrorHandler.exception_handler(e, self.table_view)

    @staticmethod
    def notification_handler(main_window: QMainWindow, success: bool) -> None:
        if success:
            main_window.tray_icon.show_notification("Export CSV", "csvSaved")
        else:
            main_window.tray_icon.show_notification("Export CSV", "saveError")

    @staticmethod
    def write_log_exception(exception: Exception) -> None:
        logger = get_logger()
        logger.error(exception, exc_info=True)