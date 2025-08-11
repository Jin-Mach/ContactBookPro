from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout, QTabWidget, QTextEdit

from src.manual.utilities.set_tab_texts import apply_tab_texts

if TYPE_CHECKING:
    from src.manual.ui.manual_widgets.manual_treewidget import ManualTreeWidget


# noinspection PyUnresolvedReferences
class ManualCheckWidget(QWidget):
    def __init__(self, tree_widget: "ManualTreeWidget", top_item_index: int, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("manualCheckWidget")
        self.tree_widget = tree_widget
        self.top_item_index = top_item_index
        self.setLayout(self.create_gui())
        tab_widgets = [self.check_birthday_text_edit, self.check_duplicity_text_edit, self.check_missing_coords_text_edit]
        apply_tab_texts(self.objectName(), self.manual_check_tab_widget, tab_widgets, self)

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.manual_check_tab_widget = QTabWidget()
        self.manual_check_tab_widget.currentChanged.connect(self.set_tree_item)
        self.check_birthday_text_edit = QTextEdit()
        self.check_birthday_text_edit.setObjectName("checkBirthdayTextEdit")
        self.check_birthday_text_edit.setReadOnly(True)
        self.check_birthday_text_edit.setText("birthday")
        self.check_duplicity_text_edit = QTextEdit()
        self.check_duplicity_text_edit.setObjectName("checkDuplicityTextEdit")
        self.check_duplicity_text_edit.setReadOnly(True)
        self.check_duplicity_text_edit.setText("duplicity")
        self.check_missing_coords_text_edit = QTextEdit()
        self.check_missing_coords_text_edit.setObjectName("checkMissingCoordsTextEdit")
        self.check_missing_coords_text_edit.setReadOnly(True)
        self.check_missing_coords_text_edit.setText("coords")
        self.manual_check_tab_widget.addTab(self.check_birthday_text_edit, "")
        self.manual_check_tab_widget.addTab(self.check_duplicity_text_edit, "")
        self.manual_check_tab_widget.addTab(self.check_missing_coords_text_edit, "")
        main_layout.addWidget(self.manual_check_tab_widget)
        return main_layout

    def set_tree_item(self) -> None:
        if not self.tree_widget.initialized:
            return
        top_item = self.tree_widget.topLevelItem(self.top_item_index)
        if top_item is None:
            return
        current_item = self.tree_widget.currentItem()
        if current_item is top_item:
            return
        tab_index = self.manual_check_tab_widget.currentIndex()
        if tab_index is not None and 0 <= tab_index < top_item.childCount():
            item_to_select = top_item.child(tab_index)
        else:
            item_to_select = top_item
        self.tree_widget.setCurrentItem(item_to_select)
        parent = item_to_select.parent()
        while parent is not None:
            parent.setExpanded(True)
            parent = parent.parent()

    def set_current_tab(self, index: int) -> None:
        self.manual_check_tab_widget.setCurrentIndex(index)