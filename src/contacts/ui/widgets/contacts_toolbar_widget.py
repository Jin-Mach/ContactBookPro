from PyQt6.QtCore import QSize
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QWidget, QLayout, QHBoxLayout, QDialog

from src.contacts.ui.dialogs.contact_dialog import ContactDialog
from src.contacts.ui.dialogs.delete_dialogs import DeleteDialogs
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


# noinspection PyUnresolvedReferences
class ContactsToolbarWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("contactsToolbarWidget")
        self.parent = parent
        self.buttons_size = QSize(35, 35)
        self.setLayout(self.create_gui())
        self.set_ui_text()

    def create_gui(self) -> QLayout:
        main_layout = QHBoxLayout()
        self.add_new_contact_pushbutton = QPushButton()
        self.add_new_contact_pushbutton.setObjectName("addNewContactPushbutton")
        self.add_new_contact_pushbutton.setFixedSize(self.buttons_size)
        self.add_new_contact_pushbutton.clicked.connect(self.add_new_contact)
        self.update_contact_pushbutton = QPushButton()
        self.update_contact_pushbutton.setObjectName("updateContactPushbutton")
        self.update_contact_pushbutton.setFixedSize(self.buttons_size)
        self.delete_contact_pushbutton = QPushButton()
        self.delete_contact_pushbutton.setObjectName("deleteContactPushbutton")
        self.delete_contact_pushbutton.setFixedSize(self.buttons_size)
        self.delete_contact_pushbutton.clicked.connect(self.delete_contact)
        self.delete_all_contacts_pushbutton = QPushButton()
        self.delete_all_contacts_pushbutton.setObjectName("deleteAllContactsPushbutton")
        self.delete_all_contacts_pushbutton.setFixedSize(self.buttons_size)
        self.delete_all_contacts_pushbutton.clicked.connect(self.delete_all_contacts)
        self.search_text_label = QLabel()
        self.search_text_label.setFont(QFont("Arial", 12))
        self.search_text_label.setObjectName("searchTextLabel")
        self.search_line_edit = QLineEdit()
        self.search_line_edit.setObjectName("searchLineEdit")
        self.search_line_edit.setFixedSize(400, 35)
        self.search_line_edit.setFont(QFont("Arial", 15))
        self.search_pushbutton = QPushButton()
        self.search_pushbutton.setObjectName("searchPushbutton")
        self.search_pushbutton.setFixedSize(self.buttons_size)
        main_layout.addWidget(self.add_new_contact_pushbutton)
        main_layout.addWidget(self.update_contact_pushbutton)
        main_layout.addWidget(self.delete_contact_pushbutton)
        main_layout.addWidget(self.delete_all_contacts_pushbutton)
        main_layout.addStretch()
        main_layout.addWidget(self.search_text_label)
        main_layout.addWidget(self.search_line_edit)
        main_layout.addWidget(self.search_pushbutton)
        main_layout.addStretch()
        return main_layout

    def set_ui_text(self) -> None:
        ui_text = LanguageProvider.get_ui_text(self.objectName())
        widgets = [self.search_text_label, self.search_line_edit]
        try:
            for widget in widgets:
                if widget.objectName() in ui_text:
                    if isinstance(widget, QLabel):
                        widget.setText(ui_text[widget.objectName()])
                    if isinstance(widget, QLineEdit):
                        widget.setPlaceholderText(ui_text[widget.objectName()])
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def add_new_contact(self) -> None:
        try:
            dialog = ContactDialog(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                dialog.accept()
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def delete_contact(self) -> None:
        try:
            dialog = DeleteDialogs.show_delete_contact_dialog(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                dialog.accept()
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def delete_all_contacts(self) -> None:
        try:
            dialog = DeleteDialogs.show_delete_all_contacts_dialog(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                dialog.accept()
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)