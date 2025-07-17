from typing import Any

from PyQt6.QtSql import QSqlDatabase, QSqlQuery

from src.statistics.utilities.mapping_keys import MapKeys
from src.utilities.error_handler import ErrorHandler


class QueryProvider:
    map_key = MapKeys

    @staticmethod
    def get_statistics_data(db_connection: QSqlDatabase, db_table: str, column_name: str) -> list[tuple[str, Any]] | None:
        try:
            data_query = QSqlQuery(db_connection)
            if not data_query.exec(f"SELECT {column_name}, COUNT (*) FROM {db_table} GROUP BY {column_name}"):
                ErrorHandler.database_error(data_query.lastError().text(), False)
                return None
            result = []
            while data_query.next():
                if column_name == "gender":
                    value = QueryProvider.map_key.mapping_keys("gender", data_query.value(0))
                    result.append((data_query.value(0), value, data_query.value(1)))
                elif column_name == "relationship":
                    value = QueryProvider.map_key.mapping_keys("relationship", data_query.value(0))
                    result.append((value, data_query.value(1)))
                elif column_name.endswith("city") or column_name.endswith("country"):
                    result.append((data_query.value(0).casefold(), data_query.value(1)))
                else:
                    result.append((data_query.value(0), data_query.value(1)))
            return result
        except Exception as e:
            ErrorHandler.exception_handler(e)
            return None