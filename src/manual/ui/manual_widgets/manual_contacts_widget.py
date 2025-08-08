from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout, QTextEdit, QTabWidget

from src.manual.utilities.set_tab_texts import apply_tab_texts


class ManualContactsWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("manualContactsWidget")
        self.setLayout(self.create_gui())
        tab_widgets = [self.add_update_contact_text_edit, self.delete_contacts_text_edit, self.search_contacts_text_edit,
                       self.context_menu_text_edit]
        apply_tab_texts(self.objectName(), self.manual_contacts_tab_widget, tab_widgets, self)

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.manual_contacts_tab_widget = QTabWidget()
        self.add_update_contact_text_edit = QTextEdit()
        self.add_update_contact_text_edit.setObjectName("addUpdateContactsTextEdit")
        self.add_update_contact_text_edit.setReadOnly(True)
        self.add_update_contact_text_edit.setText("add/edit")
        self.delete_contacts_text_edit = QTextEdit()
        self.delete_contacts_text_edit.setObjectName("deleteContactsTextEdit")
        self.delete_contacts_text_edit.setReadOnly(True)
        self.delete_contacts_text_edit.setText("delete")
        self.search_contacts_text_edit = QTextEdit()
        self.search_contacts_text_edit.setObjectName("searchContactsTextEdit")
        self.search_contacts_text_edit.setReadOnly(True)
        self.search_contacts_text_edit.setText("search")
        self.context_menu_text_edit = QTextEdit()
        self.context_menu_text_edit.setObjectName("contextMenuTextEdit")
        self.context_menu_text_edit.setReadOnly(True)
        self.context_menu_text_edit.setText("context menu")
        self.manual_contacts_tab_widget.addTab(self.add_update_contact_text_edit, "")
        self.manual_contacts_tab_widget.addTab(self.delete_contacts_text_edit, "")
        self.manual_contacts_tab_widget.addTab(self.search_contacts_text_edit, "")
        self.manual_contacts_tab_widget.addTab(self.context_menu_text_edit, "")
        main_layout.addWidget(self.manual_contacts_tab_widget)
        return main_layout

    def set_current_tab(self, index: int) -> None:
        self.manual_contacts_tab_widget.setCurrentIndex(index)