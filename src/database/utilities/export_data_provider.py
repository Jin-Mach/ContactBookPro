from typing import Any

from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import QTableView

from src.utilities.error_handler import ErrorHandler


class ExportDataProvider:
    tables = ["mandatory", "work", "social", "detail"]

    @staticmethod
    def get_export_headers(db_connection: QSqlDatabase, table_view: QTableView) -> dict[str, list[str]] | None:
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
            ErrorHandler.exception_handler(e, table_view)
            return None

    @staticmethod
    def get_filtered_data_csv(db_connection: QSqlDatabase, id_list: list, table_view: QTableView) -> list[dict[str, Any]] | None:
        try:
            headers_dict = ExportDataProvider.get_export_headers(db_connection, table_view)
            if not headers_dict:
                return None
            mandatory_headers = headers_dict["mandatory"]
            placeholders = ", ".join(["?"]*len(id_list))
            sql = f"SELECT {', '.join(mandatory_headers)} FROM mandatory WHERE id IN ({placeholders})"
            data_query = QSqlQuery(db_connection)
            data_query.prepare(sql)
            for displayed_id in id_list:
                data_query.addBindValue(displayed_id)
            if not data_query.exec():
                ErrorHandler.database_error(data_query.lastError().text(), False)
                return None
            final_data = []
            while data_query.next():
                row = {}
                for index in range(data_query.record().count()):
                    column_name = data_query.record().fieldName(index)
                    row[column_name] = data_query.value(index)
                final_data.append(row)
            return final_data
        except Exception as e:
            ErrorHandler.exception_handler(e, table_view)
            return None

    @staticmethod
    def get_all_data(db_connection: QSqlDatabase, active_filter: bool, id_list: list, table_view: QTableView) -> list[dict[str, Any]] | None:
        try:
            headers_dict = ExportDataProvider.get_export_headers(db_connection, table_view)
            if not headers_dict:
                return None
            sql = ExportDataProvider.create_sql_query(headers_dict, table_view)
            if not sql:
                return None
            data_query = QSqlQuery(db_connection)
            if active_filter and id_list:
                placeholders = ", ".join(["?"] * len(id_list))
                sql += f" WHERE m.id IN ({placeholders})"
                data_query.prepare(sql)
                for displayed_id in id_list:
                    data_query.addBindValue(displayed_id)
                if not data_query.exec():
                    ErrorHandler.database_error(data_query.lastError().text(), False)
                    return None
            else:
                if not data_query.exec(sql):
                    ErrorHandler.database_error(data_query.lastError().text(), False)
                    return None
            final_data = []
            while data_query.next():
                row = {}
                for index in range(data_query.record().count()):
                    column_name = data_query.record().fieldName(index)
                    row[column_name] = data_query.value(index)
                final_data.append(row)
            return final_data
        except Exception as e:
            ErrorHandler.exception_handler(e, table_view)
            return None

    @staticmethod
    def create_sql_query(headers_dict: dict[str, list[str]], table_view: QTableView) -> str | None:
        try:
            columns_list = []
            tables = list(headers_dict)
            sql = f"""SELECT columns FROM mandatory AS m\n"""
            for table in tables:
                alias = table[:1].lower()
                if table != "mandatory":
                    sql += f"LEFT JOIN {table} AS {alias} ON m.id = {alias}.id\n"
                for column in headers_dict[table]:
                    columns_list.append(f"{alias}.{column}")
            columns = ", ".join(columns_list)
            final_sql = sql.replace("columns", columns)
            return final_sql
        except Exception as e:
            ErrorHandler.exception_handler(e, table_view)
            return None