from PyQt6.QtSql import QSqlTableModel


def refresh_models(models: list[QSqlTableModel]) -> None:
    for model in models:
        model.select()