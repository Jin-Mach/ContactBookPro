import pathlib

from PyQt6.QtSql import QSqlDatabase, QSqlQuery

from src.utilities.error_handler import ErrorHandler


def create_db_connection(db_name: str) -> QSqlDatabase | None:
    db_path = pathlib.Path(__file__).parent.parent.joinpath("db_file")
    db_path.mkdir(parents=True, exist_ok=True)
    connection = QSqlDatabase.addDatabase("QSQLITE", "default_connection")
    connection.setDatabaseName(str(db_path.joinpath(db_name)))
    if not connection.open():
        ErrorHandler.database_error(connection.lastError().text(), True)
        return None
    query = QSqlQuery(connection)
    query.exec("PRAGMA foreign_keys = ON")
    result, query = create_contacts_tables(connection)
    if not result:
        ErrorHandler.database_error(query.lastError().text(), True)
        return None
    return connection

def create_contacts_tables(connection: QSqlDatabase) -> tuple[bool, QSqlQuery]:
    query = QSqlQuery(connection)
    create_mandatory_table = query.exec("""CREATE TABLE IF NOT EXISTS mandatory(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        gender INTEGER NOT NULL,
        relationship INTEGER NOT NULL,
        first_name TEXT NOT NULL,
        second_name TEXT NOT NULL,
        personal_email TEXT NOT NULL,
        personal_phone_number TEXT NOT NULL,
        personal_street TEXT,
        personal_house_number TEXT NOT NULL,
        personal_city TEXT NOT NULL,
        personal_post_code TEXT NOT NULL,
        personal_country TEXT NOT NULL,
        first_name_normalized TEXT,
        second_name_normalized TEXT,
        personal_street_normalized TEXT,
        personal_city_normalized TEXT,
        personal_country_normalized TEXT
        )
    """)
    create_work_table = query.exec("""CREATE TABLE IF NOT EXISTS work(
        id INTEGER PRIMARY KEY,
        company_name TEXT,
        work_email TEXT,
        work_phone_number TEXT,
        work_street TEXT,
        work_house_number TEXT,
        work_city TEXT,
        work_post_code TEXT,
        work_country TEXT,
        company_name_normalized TEXT,
        work_street_normalized TEXT,
        work_city_normalized TEXT,
        work_country_normalized TEXT,
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
        birthday DATE,
        notes TEXT,
        photo BLOB,
        title_normalized TEXT,
        notes_normalized TEXT,
        FOREIGN KEY (id) REFERENCES mandatory(id) ON DELETE CASCADE
        )
    """)
    create_info_table = query.exec("""CREATE TABLE IF NOT EXISTS info(
        id INTEGER PRIMARY KEY,
        created TEXT,
        updated TEXT,
        latitude REAL,
        longitude REAL,
        location_tries INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (id) REFERENCES mandatory(id) ON DELETE CASCADE
        )
    """)
    result = create_mandatory_table and create_work_table and create_social_table and create_detail_table and create_info_table
    return result, query