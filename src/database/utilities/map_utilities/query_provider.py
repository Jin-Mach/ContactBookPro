from typing import Any

from PyQt6.QtSql import QSqlDatabase, QSqlQuery

from src.utilities.error_handler import ErrorHandler


class QueryProvider:

    @staticmethod
    def get_maps_contacts(db_connection: QSqlDatabase) -> list[dict[str, Any]] | None:
        try:
            result = []
            query = QSqlQuery(db_connection)
            sql = ("SELECT mandatory.first_name, mandatory.second_name, mandatory.personal_email, "
                   "mandatory.personal_phone_number, info.latitude, info.longitude "
                   "FROM mandatory INNER JOIN info ON mandatory.id = info.id "
                   "WHERE (info.latitude IS NOT NULL AND info.latitude != '') "
                   "AND (info.longitude IS NOT NULL AND info.longitude != '')")
            if not query.exec(sql):
                ErrorHandler.database_error(query.lastError().text(), False)
                return None
            while query.next():
                row = {
                    "first_name": query.value(0),
                    "second_name": query.value(1),
                    "email": query.value(2),
                    "phone_number": query.value(3),
                    "latitude": query.value(4),
                    "longitude": query.value(5)
                }
                result.append(row)
            return result
        except Exception as e:
            ErrorHandler.exception_handler(e)
            return None