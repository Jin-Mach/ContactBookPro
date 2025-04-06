from PyQt6.QtSql import QSqlTableModel, QSqlDatabase


class DetailModel(QSqlTableModel):
    def __init__(self, db_connection: QSqlDatabase, parent=None) -> None:
        super().__init__(parent, db_connection)
        self.setObjectName("detailModel")
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        self.setTable("detail")