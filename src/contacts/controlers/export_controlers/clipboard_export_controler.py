from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QApplication, QMainWindow

from src.database.utilities.row_data_provider import RowDataProvider
from src.utilities.error_handler import ErrorHandler


def copy_to_clipboard(db_connection: QSqlDatabase, index: int, field: str, main_window: QMainWindow) -> None:
    try:
        clipboard = QApplication.clipboard()
        row_data = RowDataProvider.return_row_data(db_connection, index)
        if not row_data:
            return
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