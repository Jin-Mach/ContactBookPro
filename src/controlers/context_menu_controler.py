from PyQt6.QtCore import QStandardPaths
from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog, QTableView

from src.database.database_utilities.export_data_provider import ExportDataProvider
from src.database.database_utilities.row_data_provider import RowDataProvider
from src.utilities.error_handler import ErrorHandler


class ContextMenuControler:
    def __init__(self, db_connection: QSqlDatabase, table_view: QTableView) -> None:
        self.class_name = "contextMenuControler"
        self.export_path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
        self.db_connection = db_connection
        self.table_view = table_view
        self.export_data_provider = ExportDataProvider()

    @staticmethod
    def copy_to_clipboard(index: int, field: str, main_window: QMainWindow) -> None:
        try:
            clipboard = QApplication.clipboard()
            row_data = RowDataProvider.return_row_data(index)
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

    def export_to_csv(self) -> None:
        try:
            id_list = self.table_view.get_displayed_contacts_id()
            print(id_list)
            if not id_list:
                return
            data = self.export_data_provider.get_all_data(self.db_connection, True, id_list, self.table_view)
            print(data)
            # file_name,_ = QFileDialog.getSaveFileName(parent=main_window, directory=self.export_path)
            # if file_name:
            #     print(file_name)
        except Exception as e:
            ErrorHandler.exception_handler(e, self.table_view)