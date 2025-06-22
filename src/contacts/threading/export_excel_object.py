import xlsxwriter
from PyQt6.QtCore import QObject, pyqtSignal

from src.utilities.language_provider import LanguageProvider


class ExportExcelObject(QObject):
    error_message = pyqtSignal(Exception)
    finished = pyqtSignal(bool)

    def __init__(self, file_path: str, headers: dict[str, list], excel_data: dict[str, list]) -> None:
        super().__init__()
        self.class_name = "exportExcelObject"
        self.file_path = file_path
        self.headers = headers
        self.excel_data = excel_data
        _, self.index_map = LanguageProvider().get_export_settings(self.class_name)

    def run_excel_export(self) -> None:
        try:
            workbook = xlsxwriter.Workbook(self.file_path)
            headers_format = workbook.add_format({"bold": True, "align": "center"})
            data_format = workbook.add_format({"align": "center"})
            for table_key, translated_sheet_name in self.index_map.get("tables", {}).items():
                worksheet = workbook.add_worksheet(translated_sheet_name)
                headers = self.index_map.get("headers", {}).get(table_key, {})
                data_rows = self.excel_data.get(table_key, [])
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
            workbook.close()
            self.finished.emit(True)
        except Exception as e:
            self.error_message.emit(e)
            self.finished.emit(False)