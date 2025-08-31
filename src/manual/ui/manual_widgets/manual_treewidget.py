from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTreeWidget, QAbstractItemView, QTreeWidgetItem

from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class ManualTreeWidget(QTreeWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("manualTreeWidget")
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.set_headers()
        self.set_items()
        self.hide_child_items()
        self.initialized= False

    def set_headers(self) -> None:
        try:
            self.ui_text = LanguageProvider.get_json_text("ui_text.json", self.objectName())
            headers_text = self.ui_text.get("headers", "")
            if headers_text:
                self.setHeaderLabels(headers_text)
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_items(self) -> None:
        try:
            items_ui_text = self.ui_text.get("items", {})
            if items_ui_text:
                for stacked_index, key in enumerate(items_ui_text):
                    item = items_ui_text.get(key)
                    top_item = QTreeWidgetItem([item[0]])
                    top_item.setData(0, Qt.ItemDataRole.UserRole, (stacked_index, 0))
                    for tab_index, children in enumerate(item[1]):
                        child = QTreeWidgetItem([children])
                        child.setData(0, Qt.ItemDataRole.UserRole, (stacked_index, tab_index))
                        top_item.addChild(child)
                    self.addTopLevelItem(top_item)
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def hide_child_items(self) -> None:
        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            item.setExpanded(False)