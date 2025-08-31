from typing import TYPE_CHECKING

from PyQt6.QtCore import QStandardPaths
from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMainWindow, QFileDialog

from src.contacts.threading.basic_thread import BasicThread
from src.contacts.threading.objects.export_cvs_object import ExportCsvObject
from src.database.utilities.contacts_utilities.export_data_provider import ExportDataProvider
from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider

if TYPE_CHECKING:
    from src.contacts.ui.main_widgets.contacts_tableview_widget import ContactsTableviewWidget


# noinspection PyTypeChecker,PyUnresolvedReferences
class CsvExportController:
    def __init__(self, db_connection: QSqlDatabase, table_view: "ContactsTableviewWidget") -> None:
        self.class_name = "csvExportController"
        self.export_path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
        self.db_connection = db_connection
        self.table_view = table_view
        self.export_data_provider = ExportDataProvider()

    def export_filtered_to_csv(self, main_window: QMainWindow) -> None:
        try:
            id_list = self.table_view.get_displayed_contacts_id()
            if not id_list:
                error_text = LanguageProvider.get_json_text("errors_text.json", self.class_name)
                if error_text:
                    DialogsProvider.show_error_dialog(error_text.get("emptyIdList", ""), main_window)
                return
            menu_text = LanguageProvider.get_json_text("menu_text.json", self.class_name)
            file_name,_ = QFileDialog.getSaveFileName(parent=main_window, directory=self.export_path, filter=menu_text.get("csvFilter", ""))
            if file_name:
                export_object = ExportCsvObject(self.db_connection.databaseName(), file_name, id_list, self.export_data_provider, main_window)
                self.create_csv_thread(export_object, main_window)
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)

    def export_all_to_csv(self, main_window: QMainWindow) -> None:
        try:
            menu_text = LanguageProvider.get_json_text("menu_text.json", self.class_name)
            file_name, _ = QFileDialog.getSaveFileName(parent=main_window, directory=self.export_path,
                                                       filter=menu_text.get("csvFilter", ""))
            if file_name:
                export_object = ExportCsvObject(self.db_connection.databaseName(), file_name, None, self.export_data_provider, main_window)
                self.create_csv_thread(export_object, main_window)
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)

    def create_csv_thread(self, export_object: ExportCsvObject, main_window: QMainWindow) -> None:
        try:
            self.csv_object = export_object
            self.csv_thread = BasicThread()
            self.csv_thread.run_basic_thread(worker=self.csv_object, start_slot=self.csv_object.run_csv_export,
                                             on_error=lambda exception: ErrorHandler.write_log_exception(self.class_name, exception),
                                             on_finished=lambda success: CsvExportController.notification_handler(main_window, success))
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)

    @staticmethod
    def notification_handler(main_window: QMainWindow, success: bool) -> None:
        if success:
            main_window.tray_icon.show_notification("Export CSV", "exportSaved")
        else:
            main_window.tray_icon.show_notification("Export CSV", "saveError")