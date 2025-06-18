from typing import Any

from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import QMainWindow

from src.database.utilities.query_provider import QueryProvider
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
    def get_csv_data(db_connection: QSqlDatabase, id_list: list | None, main_window: QMainWindow) -> tuple[bool, list[str], list[dict[str, Any]]] | None:
        try:
            headers_dict = ExportDataProvider.get_export_headers(db_connection, main_window)
            if not headers_dict:
                return None
            mandatory_headers = headers_dict["mandatory"]
            data_query = QSqlQuery(db_connection)
            if id_list:
                placeholders = ", ".join(["?"]*len(id_list))
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
            final_data = []
            semicolon, index_map = ExportDataProvider.language_provider.get_export_settings(ExportDataProvider.class_name)
            while data_query.next():
                row = {}
                for index in range(data_query.record().count()):
                    column_name = data_query.record().fieldName(index)
                    if column_name == "gender":
                        key = index_map["genderMap"]
                        index_value = data_query.value(index)
                        row[column_name] = key[str(index_value)]
                    elif column_name == "relationship":
                        key = index_map["relationshipMap"]
                        index_value = data_query.value(index)
                        row[column_name] = key[str(index_value)]
                    else:
                        row[column_name] = data_query.value(index)
                final_data.append(row)
            return semicolon, mandatory_headers, final_data
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)
            return None

    @staticmethod
    def get_excel_data(db_connection: QSqlDatabase, id_list: list | None, main_window: QMainWindow) -> tuple[dict[str, list[str]], dict[str, list[dict[str, Any]]]] | None:
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
                rows = []
                while query.next():
                    row = {}
                    for index in range(query.record().count()):
                        column_name = query.record().fieldName(index)
                        if column_name == "gender":
                            key = index_map["genderMap"]
                            index_value = query.value(index)
                            row[column_name] = key[str(index_value)]
                        elif column_name == "relationship":
                            key = index_map["relationshipMap"]
                            index_value = query.value(index)
                            row[column_name] = key[str(index_value)]
                        else:
                            row[column_name] = query.value(index)
                    rows.append(row)
                final_data[table] = rows
            return headers_dict, final_data
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)
            return None