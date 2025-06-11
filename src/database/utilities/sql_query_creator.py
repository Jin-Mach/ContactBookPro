from PyQt6.QtSql import QSqlDatabase, QSqlQuery

from src.utilities.error_handler import ErrorHandler

def create_search_query(filters: dict, parent=None) -> tuple | None:
    try:
        if not filters:
            return None
        basic_filter = """SELECT mandatory.id FROM mandatory\n"""
        where_filter = []
        values = []
        for key in filters:
            if key != "mandatory":
                basic_filter += f"LEFT JOIN {key} ON mandatory.id = {key}.id\n"
            new_filter, value = filters[key]
            where_filter.append(new_filter)
            values.extend(value)
        final_where = " AND ".join(where_filter)
        final_filter = basic_filter + "WHERE " + final_where
        return final_filter, values
    except Exception as e:
        ErrorHandler.exception_handler(e, parent)
        return None

def create_check_duplicate_query(db_connection: QSqlDatabase, contact_id: int | None, new_email: str, new_phone_number: str, parent=None) -> list | None:
    try:
        query = QSqlQuery(db_connection)
        if contact_id is None:
            query.prepare("SELECT id, first_name, second_name, personal_email, personal_phone_number from mandatory "
                          "WHERE personal_email = ? OR personal_phone_number = ?")
            query.addBindValue(new_email)
            query.addBindValue(new_phone_number)
        else:
            query.prepare("SELECT id, first_name, second_name, personal_email, personal_phone_number from mandatory "
                          "WHERE id != ? AND (personal_email = ? OR personal_phone_number = ?)")
            query.addBindValue(contact_id)
            query.addBindValue(new_email)
            query.addBindValue(new_phone_number)
        if not query.exec():
            ErrorHandler.database_error(query.lastError().text(), False)
            return None
        results = []
        while query.next():
            row = {}
            for index in range(query.record().count()):
                column_name = query.record().fieldName(index)
                row[column_name] = query.value(index)
            results.append(row)
        return results
    except Exception as e:
        ErrorHandler.exception_handler(e, parent)
        return None