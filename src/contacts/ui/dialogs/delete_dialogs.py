from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QLineEdit


# noinspection PyUnresolvedReferences
class DeleteDialogs:

    @staticmethod
    def show_delete_contact_dialog(parent=None) -> QDialog:
        dialog = QDialog(parent)
        dialog.setObjectName("deleteContactDialog")
        dialog.setWindowTitle("Delete contact")
        dialog.setFixedSize(250, 100)
        main_layout = QVBoxLayout()
        delete_contact_text_label = QLabel("delete contact?")
        delete_contact_text_label.setObjectName("deleteContactTextLabel")
        delete_contact_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        buttons_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons_box.accepted.connect(dialog.accept)
        buttons_box.rejected.connect(dialog.reject)
        buttons_box.button(QDialogButtonBox.StandardButton.Ok).setText("Delete")
        buttons_box.button(QDialogButtonBox.StandardButton.Cancel).setText("Cancel")
        main_layout.addWidget(delete_contact_text_label)
        main_layout.addWidget(buttons_box)
        dialog.setLayout(main_layout)
        return dialog

    @staticmethod
    def show_delete_all_contacts_dialog(parent=None) -> QDialog:
        dialog = QDialog(parent)
        dialog.setObjectName("deleteAllContactsDialog")
        dialog.setWindowTitle("Delete all contacts")
        dialog.setFixedSize(250, 150)
        main_layout = QVBoxLayout()
        delete_all_contacts_text_label = QLabel("Delete all contacts?\nwrite: DELETE")
        delete_all_contacts_text_label.setObjectName("deleteAllContactsTextLabel")
        delete_all_contacts_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        delete_all_contacts_edit = QLineEdit()
        delete_all_contacts_edit.setObjectName("deleteAllContactsEdit")
        buttons_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons_box.accepted.connect(dialog.accept)
        buttons_box.rejected.connect(dialog.reject)
        buttons_box.button(QDialogButtonBox.StandardButton.Ok).setText("Delete All")
        buttons_box.button(QDialogButtonBox.StandardButton.Cancel).setText("Cancel")
        main_layout.addWidget(delete_all_contacts_text_label)
        main_layout.addWidget(delete_all_contacts_edit)
        main_layout.addWidget(buttons_box)
        dialog.setLayout(main_layout)
        return dialog