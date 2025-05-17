from typing import Optional

from PyQt6.QtSql import QSqlQuery, QSqlTableModel

from src.utilities.error_handler import ErrorHandler


class RowDataProvider:

    @staticmethod
    def return_row_data(index: int) -> Optional[dict]:
        tables = ["mandatory", "work", "social", "detail", "info"]
        all_data = {}
        for table in tables:
            row_data = RowDataProvider.return_table_data(table, index)
            if not row_data:
                return None
            all_data.update(row_data)
        return all_data

    @staticmethod
    def return_table_data(table_name: str, index: int) -> Optional[dict]:
        table_data = {}
        query = QSqlQuery()
        query.prepare(f"SELECT * FROM {table_name} WHERE id = ?")
        query.bindValue(0, index)
        if not query.exec():
            ErrorHandler.database_error(query.lastError().text(), False, custom_message="queryError")
            return None
        if query.next():
            column_count = query.record().count()
            for column in range(column_count):
                column_name = query.record().fieldName(column)
                if query.isNull(column):
                    table_data[column_name] = None
                else:
                    table_data[column_name] = query.value(column)
        return table_data

    @staticmethod
    def get_last_id(model: QSqlTableModel) -> int:
        query = QSqlQuery(model.database())
        if query.exec("SELECT last_insert_rowid()"):
            if query.next():
                return query.value(0)
        return -1

    @staticmethod
    def get_row_by_id(model: QSqlTableModel, contact_id: int) -> int:
        for row in range(model.rowCount()):
            index = model.index(row, 0)
            if model.data(index) == contact_id:
                return row
        return -1