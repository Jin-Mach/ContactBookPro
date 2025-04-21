import pathlib
from typing import Optional

from PyQt6.QtSql import QSqlDatabase, QSqlQuery

from src.utilities.error_handler import ErrorHandler


def create_db_connection(db_name: str) -> Optional[QSqlDatabase]:
    db_path = pathlib.Path(__file__).parent.parent.joinpath("db_file")
    connection = QSqlDatabase.addDatabase("QSQLITE")
    connection.setDatabaseName(str(db_path.joinpath(db_name)))
    if not connection.open():
        ErrorHandler.database_error(connection.lastError().text(), True)
        return None
    query = QSqlQuery()
    query.exec("PRAGMA foreign_keys = ON")
    result, query = create_contacts_tables()
    if not result:
        ErrorHandler.database_error(query.lastError().text(), True)
        return None
    return connection

def create_contacts_tables() -> tuple[bool, QSqlQuery]:
    query = QSqlQuery()
    create_mandatory_table = query.exec("""CREATE TABLE IF NOT EXISTS mandatory(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        gender TEXT NOT NULL,
        relationship INTEGER NOT NULL,
        first_name TEXT NOT NULL,
        second_name TEXT NOT NULL,
        personal_email TEXT NOT NULL,
        personal_phone_number TEXT NOT NULL,
        personal_city TEXT NOT NULL,
        personal_street TEXT NOT NULL,
        personal_house_number TEXT,
        personal_post_code TEXT NOT NULL,
        personal_country TEXT NOT NULL
        )
    """)
    create_work_table = query.exec("""CREATE TABLE IF NOT EXISTS work(
        id INTEGER PRIMARY KEY,
        company_name TEXT,
        work_email TEXT,
        work_phone_number TEXT,
        work_city TEXT,
        work_street TEXT,
        work_house_number TEXT,
        work_post_code TEXT,
        work_country TEXT,
        FOREIGN KEY (id) REFERENCES mandatory(id) ON DELETE CASCADE
        )
    """)
    create_social_table = query.exec("""CREATE TABLE IF NOT EXISTS social(
        id INTEGER PRIMARY KEY,
        facebook_url TEXT,
        x_url TEXT,
        instagram_url TEXT,
        linkedin_url TEXT,
        github_url TEXT,
        website_url TEXT,
        FOREIGN KEY (id) REFERENCES mandatory(id) ON DELETE CASCADE
        )
    """)
    create_detail_table = query.exec("""CREATE TABLE IF NOT EXISTS detail(
        id INTEGER PRIMARY KEY,
        title TEXT,
        birthday TEXT,
        notes TEXT,
        photo BLOB,
        FOREIGN KEY (id) REFERENCES mandatory(id) ON DELETE CASCADE
        )
    """)
    create_info_table = query.exec("""CREATE TABLE IF NOT EXISTS info(
        id INTEGER PRIMARY KEY,
        created TEXT,
        updated TEXT,
        latitude REAL,
        longitude REAL,
        FOREIGN KEY (id) REFERENCES mandatory(id) ON DELETE CASCADE
        )
    """)
    result = create_mandatory_table and create_work_table and create_social_table and create_detail_table and create_info_table
    return result, query