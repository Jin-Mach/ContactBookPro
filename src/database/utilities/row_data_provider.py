from PyQt6.QtSql import QSqlQuery, QSqlTableModel, QSqlDatabase

from src.utilities.error_handler import ErrorHandler


class RowDataProvider:

    @staticmethod
    def return_row_data(db_connection: QSqlDatabase, index: int) -> dict | None:
        tables = ["mandatory", "work", "social", "detail", "info"]
        all_data = {}
        for table in tables:
            row_data = RowDataProvider.return_table_data(db_connection, table, index)
            if not row_data:
                return None
            all_data.update(row_data)
        return all_data

    @staticmethod
    def return_table_data(db_connection: QSqlDatabase, table_name: str, index: int) -> dict | None:
        table_data = {}
        query = QSqlQuery(db_connection)
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