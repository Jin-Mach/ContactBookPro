from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import QMainWindow

from src.utilities.error_handler import ErrorHandler


class QueryProvider:

    @staticmethod
    def create_search_query(filters: dict, parent=None) -> tuple[str, list] | None:
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

    @staticmethod
    def create_check_duplicate_query(db_connection: QSqlDatabase, contact_id: int | None, new_email: str, new_phone_number: str, parent=None) -> list[dict]| None:
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

    @staticmethod
    def create_excel_query(headers_dict: dict[str, list[str]], id_list: list | None, main_window: QMainWindow) -> dict[str, str] | None:
        try:
            sql_dict = {}
            for table, columns in headers_dict.items():
                columns_str = ", ".join(columns)
                sql = f"SELECT {columns_str} FROM {table}"
                if id_list:
                    placeholders = ", ".join(["?"] * len(id_list))
                    sql += f" WHERE id IN ({placeholders})"
                sql_dict[table] = sql
            return sql_dict
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)
            return None

    @staticmethod
    def create_pdf_list_query(id_list: list | None, main_window: QMainWindow) -> str | None:
        try:
            sql = ("SELECT gender, relationship, first_name, second_name, personal_email, personal_phone_number,"
                   "personal_street, personal_house_number, personal_city, personal_post_code, personal_country "
                   "FROM mandatory")
            if id_list is not None:
                placeholders = ", ".join(["?"] * len(id_list))
                sql += f" WHERE id IN ({placeholders})"
            sql += " ORDER BY second_name ASC"
            return sql
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)
            return None

    @staticmethod
    def create_check_birthday_query(db_connection: QSqlDatabase, main_window: QMainWindow) -> list[dict[str, int | str]] | None:
        try:
            ids = []
            detail_query = QSqlQuery(db_connection)
            if not detail_query.exec("SELECT id from detail "
                                     "WHERE birthday IS NOT NULL "
                                     "AND ("
                                     "julianday('now') - julianday(strftime('%Y', 'now') || '-' || strftime('%m-%d', birthday))"
                                     ") BETWEEN -7 AND 7"):
                ErrorHandler.database_error(detail_query.lastError().text(), False)
                return None
            while detail_query.next():
                ids.append(str(detail_query.value(0)))
            if not ids:
                return []
            contacts_query = QSqlQuery(db_connection)
            str_ids = ', '.join(ids)
            query = f"SELECT id, first_name, second_name FROM mandatory WHERE id IN ({str_ids})"
            if not contacts_query.exec(query):
                ErrorHandler.database_error(contacts_query.lastError().text(), False)
                return None
            results = []
            while contacts_query.next():
                row = {
                    "id": contacts_query.value(0),
                    "first_name": contacts_query.value(1),
                    "second_name": contacts_query.value(2)
                }
                results.append(row)
            return results
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)
            return None

    @staticmethod
    def create_check_duplicates_query(db_connection: QSqlDatabase, main_window: QMainWindow) -> list[dict[str, int | str]] | None:
        try:
            duplicates_query = QSqlQuery(db_connection)
            if not duplicates_query.exec("""SELECT id, first_name, second_name FROM mandatory 
                                                    WHERE personal_email IN 
                                                    (SELECT personal_email FROM mandatory GROUP BY personal_email HAVING COUNT(*) > 1) 
                                                    OR personal_phone_number IN 
                                                    (SELECT personal_phone_number FROM mandatory GROUP BY personal_phone_number HAVING COUNT(*) > 1)
                                                """):
                ErrorHandler.database_error(duplicates_query.lastError().text(), False)
                return None
            results = []
            while duplicates_query.next():
                row = {
                    "id": duplicates_query.value(0),
                    "first_name": duplicates_query.value(1),
                    "second_name": duplicates_query.value(2)
                }
                results.append(row)
            return results
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)
            return None

    @staticmethod
    def create_update_locations_query(db_connection: QSqlDatabase, main_window: QMainWindow) -> list[tuple[int, str, str, str, str, str]] | None:
        try:
            location_query = QSqlQuery(db_connection)
            sql = ("SELECT info.id, mandatory.personal_street, mandatory.personal_house_number, mandatory.personal_city, "
                   "mandatory.personal_post_code, mandatory.personal_country "
                   "FROM mandatory JOIN info ON mandatory.id = info.id "
                   "WHERE info.location_tries < 20 "
                   "AND (info.latitude IS NULL OR info.latitude = '') "
                   "AND (info.longitude IS NULL OR info.longitude = '')")
            if not location_query.exec(sql):
                ErrorHandler.database_error(location_query.lastError().text(), False)
                return None
            results = []
            while location_query.next():
                contact_id = location_query.value(0)
                street = location_query.value(1)
                house_number = location_query.value(2)
                city = location_query.value(3)
                post_code = location_query.value(4)
                country = location_query.value(5)
                results.append((contact_id, street, house_number, city, post_code, country))
            return results
        except Exception as e:
            ErrorHandler.exception_handler(e, main_window)
            return None