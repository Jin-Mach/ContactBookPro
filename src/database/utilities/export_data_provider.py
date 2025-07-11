from typing import Any

from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import QMainWindow

from src.database.utilities.query_provider import QueryProvider
from src.database.utilities.row_data_provider import RowDataProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class ExportDataProvider:
    class_name = "exportDataProvider"
    tables = ["mandatory", "work", "social", "detail"]
    language_provider = LanguageProvider()

    @staticmethod
    def get_export_headers(db_connection: QSqlDatabase, main_window: QMainWindow) -> dict[str, list[str]] | None:
        try:
            not_needed = ["id", "photo"]
            headers_by_table = {}
            for table in ExportDataProvider.tables:
                headers_query = QSqlQuery(db_connection)
                sql = f"PRAGMA table_info({table})"
                if not headers_query.exec(sql):
                    ErrorHandler.database_error(headers_query.lastError().text(), False)
                    return None
                headers = []
                while headers_query.next():
                    column = headers_query.value(1)
                    if column not in not_needed and not column.endswith("_normalized"):
                        headers.append(column)
                headers_by_table[table] = headers
            return headers_by_table
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)
            return None

    @staticmethod
    def map_value(column_name: str, value: any, index_map: dict | None) -> any:
        if not index_map:
            return value
        mapping_key = f"{column_name}Map"
        if mapping_key in index_map:
            return index_map[mapping_key].get(str(value), "")
        return value

    @staticmethod
    def get_csv_data(db_connection: QSqlDatabase, id_list: list | None, main_window: QMainWindow) -> tuple[bool, list[str], list[dict[str, Any]]] | None:
        try:
            headers_dict = ExportDataProvider.get_export_headers(db_connection, main_window)
            if not headers_dict:
                return None
            mandatory_headers = headers_dict["mandatory"]
            data_query = QSqlQuery(db_connection)
            if id_list:
                placeholders = ", ".join(["?"] * len(id_list))
                sql = f"SELECT {', '.join(mandatory_headers)} FROM mandatory WHERE id IN ({placeholders})"
                data_query.prepare(sql)
                for displayed_id in id_list:
                    data_query.addBindValue(displayed_id)
            else:
                sql = f"SELECT {', '.join(mandatory_headers)} FROM mandatory"
                data_query.prepare(sql)
            if not data_query.exec():
                ErrorHandler.database_error(data_query.lastError().text(), False)
                return None
            semicolon, index_map = ExportDataProvider.language_provider.get_export_settings(ExportDataProvider.class_name)
            if not index_map:
                index_map = {}
            final_data = []
            while data_query.next():
                row = {}
                for index in range(data_query.record().count()):
                    column_name = data_query.record().fieldName(index)
                    value = data_query.value(index)
                    row[column_name] = ExportDataProvider.map_value(column_name, value, index_map)
                final_data.append(row)
            return semicolon, mandatory_headers, final_data
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)
            return None

    @staticmethod
    def get_excel_data(db_connection: QSqlDatabase, id_list: list | None, main_window: QMainWindow) -> dict[str, list[dict[str, Any]]] | None:
        try:
            headers_dict = ExportDataProvider.get_export_headers(db_connection, main_window)
            if not headers_dict:
                return None
            sql_dict = QueryProvider.create_excel_query(headers_dict, id_list, main_window)
            if not sql_dict:
                return None
            final_data = {}
            for table, sql in sql_dict.items():
                query = QSqlQuery(db_connection)
                query.prepare(sql)
                if id_list:
                    for displayed_id in id_list:
                        query.addBindValue(displayed_id)
                if not query.exec():
                    ErrorHandler.database_error(query.lastError().text(), False)
                    return None
                _, index_map = ExportDataProvider.language_provider.get_export_settings(ExportDataProvider.class_name)
                if not index_map:
                    index_map = {}
                rows = []
                while query.next():
                    row = {}
                    for index in range(query.record().count()):
                        column_name = query.record().fieldName(index)
                        value = query.value(index)
                        row[column_name] = ExportDataProvider.map_value(column_name, value, index_map)
                    rows.append(row)
                final_data[table] = rows
            return final_data
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)
            return None

    @staticmethod
    def get_pdf_list_data(db_connection: QSqlDatabase, id_list: list | None, main_window: QMainWindow) -> list[dict[str, str]] | None:
        try:
            sql = QueryProvider.create_pdf_list_query(id_list, main_window)
            if not sql:
                return None
            query = QSqlQuery(db_connection)
            query.prepare(sql)
            if id_list is not None:
                for id_value in id_list:
                    query.addBindValue(id_value)
            if not query.exec():
                ErrorHandler.database_error(query.lastError().text(), False)
                return None
            _, index_map = ExportDataProvider.language_provider.get_export_settings(ExportDataProvider.class_name)
            if not index_map:
                index_map = {}
            results = []
            while query.next():
                row = {}
                for index in range(query.record().count()):
                    column_name = query.record().fieldName(index)
                    value = query.value(index)
                    row[column_name] = ExportDataProvider.map_value(column_name, value, index_map)
                results.append(row)
            return results
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)
            return None

    @staticmethod
    def get_pdf_contact_data(db_connection: QSqlDatabase, index: int, main_window: QMainWindow) -> dict[str, Any] | None:
        try:
            contact_data = RowDataProvider.return_row_data(db_connection, index)
            _, index_map = ExportDataProvider.language_provider.get_export_settings(ExportDataProvider.class_name)
            if not index_map:
                index_map = {}
            row = {}
            for column_name in contact_data.keys():
                value = contact_data.get(column_name, "")
                row[column_name] = ExportDataProvider.map_value(column_name, value, index_map)
            return row
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)
            return  None
