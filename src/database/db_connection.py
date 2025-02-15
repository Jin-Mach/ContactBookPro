import pathlib

from PyQt6.QtSql import QSqlDatabase, QSqlQuery


def create_db_connection(db_name: str) -> bool:
    db_path = pathlib.Path(__file__).parent.parent.joinpath("db_file")
    connection = QSqlDatabase.addDatabase("QSQLITE")
    connection.setDatabaseName(str(db_path.joinpath(db_name)))
    if not connection.open():
        print(f"connection error: {connection.lastError().text()}")
        return False
    if not create_contacts_table():
        print("error creating table")
        return False
    return True

def create_contacts_table() -> bool:
    querry = QSqlQuery()
    table_created = querry.exec("""CREATE TABLE IF NOT EXISTS contacts(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        first_name TEXT NOT NULL,
        second_name TEXT NOT NULL,
        relationship TEXT NOT NULL,
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
    if not table_created:
        print(f"error: {querry.lastError().text()}")
    return table_created