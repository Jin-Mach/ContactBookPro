from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout, QTextEdit, QTabWidget

from src.manual.utilities.set_tab_texts import apply_tab_texts
from src.manual.utilities.set_text_edits import initialize_text_edits

if TYPE_CHECKING:
    from src.manual.ui.manual_widgets.manual_treewidget import ManualTreeWidget


# noinspection PyUnresolvedReferences
class ManualContactsWidget(QWidget):
    def __init__(self, tree_widget: "ManualTreeWidget", top_item_index: int, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("manualContactsWidget")
        self.tree_widget = tree_widget
        self.top_item_index = top_item_index
        self.setLayout(self.create_gui())
        tab_widgets = [self.add_update_contact_text_edit, self.delete_contacts_text_edit, self.search_contacts_text_edit,
                       self.context_menu_text_edit]
        apply_tab_texts(self.objectName(), self.manual_contacts_tab_widget, tab_widgets, self)
        initialize_text_edits(tab_widgets, self)

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.manual_contacts_tab_widget = QTabWidget()
        self.manual_contacts_tab_widget.currentChanged.connect(self.set_tree_item)
        self.add_update_contact_text_edit = QTextEdit()
        self.add_update_contact_text_edit.setObjectName("addUpdateContactsTextEdit")
        self.delete_contacts_text_edit = QTextEdit()
        self.delete_contacts_text_edit.setObjectName("deleteContactsTextEdit")
        self.search_contacts_text_edit = QTextEdit()
        self.search_contacts_text_edit.setObjectName("searchContactsTextEdit")
        self.context_menu_text_edit = QTextEdit()
        self.context_menu_text_edit.setObjectName("contextMenuTextEdit")
        self.manual_contacts_tab_widget.addTab(self.add_update_contact_text_edit, "")
        self.manual_contacts_tab_widget.addTab(self.delete_contacts_text_edit, "")
        self.manual_contacts_tab_widget.addTab(self.search_contacts_text_edit, "")
        self.manual_contacts_tab_widget.addTab(self.context_menu_text_edit, "")
        main_layout.addWidget(self.manual_contacts_tab_widget)
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
        tab_index = self.manual_contacts_tab_widget.currentIndex()
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
        self.manual_contacts_tab_widget.setCurrentIndex(index)