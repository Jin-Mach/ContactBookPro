from typing import Any

from PyQt6.QtSql import QSqlDatabase, QSqlQuery

from src.statistics.utilities.mapping_keys import MapKeys
from src.utilities.error_handler import ErrorHandler


class QueryProvider:
    map_key = MapKeys

    @staticmethod
    def get_basic_statistics_data(db_connection: QSqlDatabase, column_name: str) -> list[tuple[str, Any]] | None:
        try:
            data_query = QSqlQuery(db_connection)
            sql = f"SELECT {column_name}, COUNT (*) FROM mandatory GROUP BY {column_name}"
            if column_name.endswith("city"):
                sql = f"SELECT LOWER({column_name}), COUNT (*) FROM mandatory GROUP BY LOWER({column_name})"
            if not data_query.exec(sql):
                ErrorHandler.database_error(data_query.lastError().text(), False)
                return None
            result = []
            while data_query.next():
                if column_name == "gender":
                    value = QueryProvider.map_key.mapping_keys("gender", str(data_query.value(0)))
                    result.append((data_query.value(0), value, data_query.value(1)))
                elif column_name == "relationship":
                    value = QueryProvider.map_key.mapping_keys("relationship", str(data_query.value(0)))
                    result.append((data_query.value(0), value, data_query.value(1)))
                elif column_name.endswith("city"):
                    result.append((str(data_query.value(0).casefold()), data_query.value(1)))
                else:
                    result.append((data_query.value(0), data_query.value(1)))
            return result
        except Exception as e:
            ErrorHandler.exception_handler(e)
            return None

    @staticmethod
    def get_work_statistics_data(db_connection: QSqlDatabase, column_name: str) -> list[tuple[str, Any]] | None:
        try:
            result = []
            data_query = QSqlQuery(db_connection)
            data_query_city = QSqlQuery(db_connection)
            data_query_count = QSqlQuery(db_connection)
            if column_name.endswith("city"):
                sql_city = (f"SELECT LOWER({column_name}), COUNT(*) FROM work "
                            f"WHERE {column_name} IS NOT NULL AND {column_name} != '' "
                            f"GROUP BY LOWER({column_name})")
                sql_count = (f"SELECT "
                            f"SUM(CASE WHEN {column_name} IS NULL OR {column_name} = '' THEN 1 ELSE 0 END) AS empty "
                            f"FROM work")
                if not data_query_city.exec(sql_city):
                    ErrorHandler.database_error(data_query_city.lastError().text(), False)
                    return None
                city_data = []
                while data_query_city.next():
                    city_data.append((str(data_query_city.value(0).casefold()), data_query_city.value(1)))
                if not data_query_count.exec(sql_count):
                    ErrorHandler.database_error(data_query_count.lastError().text(), False)
                    return None
                count_data = []
                if data_query_count.next():
                    count_data.append(data_query_count.value(0))
                result.append(city_data)
                result.append(count_data)
            else:
                sql = (f"SELECT "
                       f"SUM(CASE WHEN {column_name} IS NOT NULL AND {column_name} != '' THEN 1 ELSE 0 END) AS filled, "
                       f"SUM(CASE WHEN {column_name} IS NULL OR {column_name} = '' THEN 1 ELSE 0 END) AS empty "
                       f"FROM work")
                if not data_query.exec(sql):
                    ErrorHandler.database_error(data_query.lastError().text(), False)
                    return None
                while data_query.next():
                    filled = data_query.value(0)
                    empty = data_query.value(1)
                    result.append(("filled", filled))
                    result.append(("empty", empty))
            return result
        except Exception as e:
            ErrorHandler.exception_handler(e)
            return None

    @staticmethod
    def get_social_statistics_data(db_connection) -> dict[str, tuple[int, int]] | None:
        try:
            result = {}
            data_query = QSqlQuery(db_connection)
            columns = ["facebook", "x", "instagram", "linkedin", "github", "website"]
            sql_parts = []
            for column in columns:
                sql_parts.append(f"SUM(CASE WHEN {column}_url IS NOT NULL AND {column}_url != '' THEN 1 ELSE 0 END) AS {column}")
                sql_parts.append(f"SUM (CASE WHEN {column}_url IS NULL OR {column}_url = '' THEN 1 ELSE 0 END) AS {column}")
            sql = "SELECT " + ", ".join(sql_parts) + " FROM social"
            if not data_query.exec(sql):
                ErrorHandler.database_error(data_query.lastError().text(), False)
                return None
            while data_query.next():
                record = data_query.record()
                for i in range(0, record.count(), 2):
                    key = record.fieldName(i)
                    filled = data_query.value(i)
                    empty = data_query.value(i + 1)
                    result[key] = (filled, empty)
            return result
        except Exception as e:
            ErrorHandler.exception_handler(e)
            return None