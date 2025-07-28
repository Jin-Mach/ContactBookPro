from typing import Any

from PyQt6.QtCore import Qt, QModelIndex
from PyQt6.QtGui import QIcon
from PyQt6.QtSql import QSqlTableModel, QSqlDatabase

from src.database.utilities.contacts_utilities.model_header_provider import ModelHeaderProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.icon_provider import IconProvider
from src.utilities.language_provider import LanguageProvider


# noinspection PyTypeChecker
class MandatoryModel(QSqlTableModel):
    def __init__(self, db_connection: QSqlDatabase, parent=None) -> None:
        super().__init__(parent, db_connection)
        self.setObjectName("mandatoryModel")
        self.setTable("mandatory")
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        self.setSort(0, Qt.SortOrder.AscendingOrder)
        ModelHeaderProvider.set_mandatory_model_headers(self)
        self.icons_path = IconProvider.icons_path.joinpath("personalTabInfoWidget")
        self.male_icon = str(self.icons_path.joinpath("male_icon.png"))
        self.female_icon = str(self.icons_path.joinpath("female_icon.png"))
        self.relationship = LanguageProvider.get_ui_text("personalTabInfoWidget")
        self.gender_header_text = LanguageProvider.get_ui_text(self.objectName())["genderHeaderText"]
        self.select()

    def headerData(self, section: int, orientation: Qt.Orientation, role=Qt.ItemDataRole.DisplayRole) -> bool:
        if role == Qt.ItemDataRole.ToolTipRole:
            if orientation == Qt.Orientation.Horizontal:
                if section == 1:
                    return self.gender_header_text
        return super().headerData(section, orientation, role)

    def data(self, index: QModelIndex, role=Qt.ItemDataRole.DisplayRole) -> Any:
        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == 1:
                return ""
            elif index.column() == 2:
                value = super().data(self.index(index.row(), 2), role)
                if self.relationship:
                    relationship_dict = self.relationship.get("relationship_key", {})
                    return relationship_dict.get(str(value), "")
            elif index.column() == 3:
                first_name = super().data(self.index(index.row(), 3), role)
                second_name = super().data(self.index(index.row(), 4), role)
                return f"{first_name} {second_name}"
            elif index.column() == 4:
                return super().data(self.index(index.row(), 5), role)
            elif index.column() == 5:
                return super().data(self.index(index.row(), 6), role)
            elif index.column() == 6:
                street = super().data(self.index(index.row(), 7), role)
                house_number = super().data(self.index(index.row(), 8), role)
                city = super().data(self.index(index.row(), 9), role)
                post_code = super().data(self.index(index.row(), 10), role)
                country = super().data(self.index(index.row(), 11), role)
                if not street:
                    return f"{city}, {house_number}, {city}, {post_code}, {country}"
                return f"{street}, {house_number}, {city}, {post_code}, {country}"
        if role == Qt.ItemDataRole.DecorationRole:
            if index.column() == 1:
                value = super().data(self.index(index.row(), 1), Qt.ItemDataRole.DisplayRole)
                if value == 1:
                    return QIcon(self.male_icon)
                else:
                    return QIcon(self.female_icon)
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter
        return super().data(index, role)

    def add_contact(self, data: list) -> None:
        record = self.record()
        for index, value in enumerate(data):
            record.setValue(index + 1, value)
        self.insertRecord(-1, record)
        if not self.submitAll():
            ErrorHandler.database_error(self.lastError().text(), False, custom_message="queryError")
            return

    def update_contact(self, row_index: int, data: list) -> None:
        column_count = self.columnCount()
        for column in range(1, column_count):
            index = self.index(row_index, column)
            self.setData(index, data[column - 1])
        if not self.submitAll():
            ErrorHandler.database_error(self.lastError().text(), False, custom_message="queryError")
            return

    def delete_contact(self, row_index: int) -> None:
        if row_index > -1:
            if not self.removeRow(row_index):
                ErrorHandler.database_error(self.lastError().text(), False, custom_message="queryError")
                return
            if not self.submitAll():
                ErrorHandler.database_error(self.lastError().text(), False, custom_message="queryError")
                return

    def clear_database(self) -> None:
        if self.rowCount() > 0:
            if not self.removeRows(0, self.rowCount()):
                ErrorHandler.database_error(self.lastError().text(), False, custom_message="queryError")
                return
        self.select()

    def set_filter_by_id(self, id_list: list) -> None:
        map_list = ",".join(map(str, id_list))
        self.setFilter(f"id IN ({map_list})")
        self.select()