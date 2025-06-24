import xlsxwriter
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMainWindow

from src.database.utilities.export_data_provider import ExportDataProvider
from src.utilities.language_provider import LanguageProvider


class ExportExcelObject(QObject):
    error_message = pyqtSignal(Exception)
    finished = pyqtSignal(bool)

    def __init__(self, db_path: str, file_path: str, id_list: list | None, export_data_provider: ExportDataProvider,
                 main_window: QMainWindow) -> None:
        super().__init__()
        self.class_name = "exportExcelObject"
        self.db_path = db_path
        self.file_path = file_path
        self.id_list = id_list
        self.export_data_provider = export_data_provider
        self.main_window = main_window
        _, self.index_map = LanguageProvider().get_export_settings(self.class_name)
        self.connection_name = f"exportExcelThread{id(self)}"

    def run_excel_export(self) -> None:
        db_connection = None
        try:
            db_connection = QSqlDatabase.addDatabase("QSQLITE", self.connection_name)
            db_connection.setDatabaseName(self.db_path)
            if not db_connection.open():
                self.finished.emit(False)
                return
            workbook = xlsxwriter.Workbook(self.file_path)
            headers_format = workbook.add_format({"bold": True, "align": "center"})
            data_format = workbook.add_format({"align": "center"})
            excel_data = self.export_data_provider.get_excel_data(db_connection, self.id_list, self.main_window)
            if not excel_data:
                self.finished.emit(False)
                return
            for table_key, translated_sheet_name in self.index_map.get("tables", {}).items():
                worksheet = workbook.add_worksheet(translated_sheet_name)
                headers = self.index_map.get("headers", {}).get(table_key, {})
                data_rows = excel_data.get(table_key, [])
                for col_index, header_name in enumerate(headers.values()):
                    max_length = len(header_name)
                    for row in data_rows:
                        cell_value = str(row.get(list(headers.keys())[col_index], ""))
                        max_length = max(max_length, len(cell_value))
                    worksheet.write(0, col_index, header_name, headers_format)
                    worksheet.set_column(col_index, col_index, max_length + 2)
                for row_index, row_data in enumerate(data_rows, start=1):
                    for col_index, field_key in enumerate(headers.keys()):
                        value = row_data.get(field_key, "")
                        if value == "":
                            value = "N/A"
                            worksheet.write(row_index, col_index, value, data_format)
                        elif field_key.endswith("_email") and value != "N/A":
                            url = value
                            if not url.startswith("mailto:"):
                                url = "mailto:" + url
                            worksheet.write_url(row_index, col_index, url, cell_format=data_format)
                        elif field_key.endswith('_url') and value != "N/A":
                            url = value
                            if not url.startswith(("http://", "https://")):
                                url = "http://" + url
                            worksheet.write_url(row_index, col_index, url, cell_format=data_format)
                        else:
                            worksheet.write(row_index, col_index, value, data_format)
            try:
                workbook.close()
            except Exception as e:
                self.error_message.emit(e)
                self.finished.emit(False)
                return
            self.finished.emit(True)
        except Exception as e:
            self.error_message.emit(e)
            self.finished.emit(False)
        finally:
            if db_connection:
                db_connection.close()
                QSqlDatabase.removeDatabase(self.connection_name)