import pathlib

from PyQt6.QtSql import QSqlDatabase

from src.database.db_connection import create_db_connection


def reset_database() -> bool:
    db_path = pathlib.Path(__file__).parents[3].joinpath("db_file")
    db_name = None
    for item in db_path.iterdir():
        if item.is_file() and item.name.endswith(".sqlite"):
            db_name = item.name
            break
    if db_name is None:
        return False
    db_path = db_path.joinpath(db_name)
    database = QSqlDatabase.database("default_connection")
    if database.isOpen():
        database.close()
    del database
    QSqlDatabase.removeDatabase("default_connection")
    db_path.unlink()
    create_db_connection(db_name)
    return True