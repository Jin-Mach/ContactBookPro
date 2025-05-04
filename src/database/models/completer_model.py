from PyQt6.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import QLineEdit

from src.utilities.error_handler import ErrorHandler


class CompleterModel(QSqlQueryModel):
    def __init__(self, db_connection: QSqlDatabase, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("CompleterModel")
        self.db_connection = db_connection

    def get_data(self, column_index: int, line_edit: QLineEdit) -> None:
        text = line_edit.text().strip()
        query_sql = {
            "3": "SELECT first_name || ' ' || second_name AS full_name FROM mandatory ORDER BY full_name ASC",
            "4": f"SELECT personal_email FROM mandatory WHERE personal_email LIKE '%{text}%' ORDER BY personal_email ASC",
            "5": f"SELECT personal_phone_number FROM mandatory WHERE personal_phone_number LIKE '%{text}%' ORDER BY personal_phone_number ASC",
            "6": """
                    SELECT 
                        personal_city || ', ' || 
                        COALESCE(personal_street || ', ', '') || 
                        personal_house_number || ', ' || 
                        personal_post_code || ', ' || 
                        personal_country AS full_address 
                        FROM mandatory
                        ORDER BY full_address ASC
                    """
        }
        if column_index is not None and str(column_index) in query_sql:
            sql = query_sql[str(column_index)]
            completer_query = QSqlQuery(self.db_connection)
            completer_query.prepare(sql)
            if not completer_query.exec():
                ErrorHandler.database_error(completer_query.lastError().text(), False)
            self.setQuery(completer_query)