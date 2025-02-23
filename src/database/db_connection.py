import pathlib
import sys
from typing import Optional

from PyQt6.QtSql import QSqlDatabase, QSqlQuery

from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.language_provider import LanguageProvider
from src.utilities.logger_provider import get_logger


def create_db_connection(db_name: str) -> Optional[QSqlDatabase]:
    db_path = pathlib.Path(__file__).parent.parent.joinpath("db_file")
    connection = QSqlDatabase.addDatabase("QSQLITE")
    connection.setDatabaseName(str(db_path.joinpath(db_name)))
    if not connection.open():
        log_and_show_error(connection.lastError().text())
        return None
    result, query = create_contacts_table()
    if not result:
        log_and_show_error(query.lastError().text())
        return None
    return connection

def create_contacts_table() -> tuple[bool, QSqlQuery]:
    query = QSqlQuery()
    create_table = query.exec("""CREATE TABLE IF NOT EXISTS contacts(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        relationship TEXT NOT NULL,
        first_name TEXT NOT NULL,
        second_name TEXT NOT NULL,
        personal_email TEXT NOT NULL,
        personal_phone_number TEXT NOT NULL,
        personal_address TEXT NOT NULL,
        personal_city TEXT NOT NULL,
        personal_post_code TEXT NOT NULL,
        personal_country TEXT NOT NULL,
        work_email TEXT,
        work_phone_number TEXT,
        work_address TEXT,
        work_city TEXT,
        work_post_code TEXT,
        work_country TEXT,
        facebook_url TEXT,
        x_url TEXT,
        instagram_url TEXT,
        linkedin_url TEXT,
        github_url TEXT,
        website_url TEXT,
        title TEXT,
        birthday DATE,
        notes TEXT,
        photo BLOB,
        latitude REAL,
        longitude REAL
        )
    """)
    return create_table, query

def log_and_show_error(error_message: str) -> None:
    logger = get_logger()
    logger.error(error_message)
    error = LanguageProvider.get_error_text("errorHandler")
    DialogsProvider.show_database_error_dialog(error["DatabaseConnectionError"])
    sys.exit(1)