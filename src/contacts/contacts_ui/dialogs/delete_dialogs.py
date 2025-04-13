from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QLineEdit, QPushButton

from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


# noinspection PyUnresolvedReferences
class DeleteDialogs:
    class_name = "deleteDialogWidgets"

    @staticmethod
    def show_delete_contact_dialog(parent=None) -> QDialog:
        dialog = QDialog(parent)
        dialog.setObjectName("deleteContactDialog")
        dialog.setFixedSize(200, 100)
        main_layout = QVBoxLayout()
        delete_contact_text_label = QLabel()
        delete_contact_text_label.setObjectName("deleteContactTextLabel")
        delete_contact_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        buttons_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons_box.accepted.connect(dialog.accept)
        buttons_box.rejected.connect(dialog.reject)
        delete_contact_button = buttons_box.button(QDialogButtonBox.StandardButton.Ok)
        delete_contact_button.setObjectName("deleteContactButton")
        cancel_contact_button = buttons_box.button(QDialogButtonBox.StandardButton.Cancel)
        cancel_contact_button.setObjectName("cancelContactButton")
        main_layout.addWidget(delete_contact_text_label)
        main_layout.addWidget(buttons_box)
        dialog.setLayout(main_layout)
        DeleteDialogs.set_ui_text(dialog, delete_contact_text_label, buttons_box)
        return dialog

    @staticmethod
    def show_delete_all_contacts_dialog(parent=None) -> QDialog:
        dialog = QDialog(parent)
        dialog.setObjectName("deleteAllContactsDialog")
        dialog.setFixedSize(300, 150)
        main_layout = QVBoxLayout()
        delete_all_contacts_text_label = QLabel()
        delete_all_contacts_text_label.setObjectName("deleteAllContactsTextLabel")
        delete_all_contacts_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        delete_all_contacts_edit = QLineEdit()
        delete_all_contacts_edit.setObjectName("deleteAllContactsEdit")
        buttons_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons_box.button(QDialogButtonBox.StandardButton.Ok).clicked.connect(lambda: DeleteDialogs.delete_accepted(dialog,
                            delete_all_contacts_text_label,delete_all_contacts_edit))
        buttons_box.rejected.connect(dialog.reject)
        delete_all_contacts_button = buttons_box.button(QDialogButtonBox.StandardButton.Ok)
        delete_all_contacts_button.setObjectName("deleteAllContactsButton")
        cancel_all_contacts_button = buttons_box.button(QDialogButtonBox.StandardButton.Cancel)
        cancel_all_contacts_button.setObjectName("cancelAllContactsButton")
        main_layout.addWidget(delete_all_contacts_text_label)
        main_layout.addWidget(delete_all_contacts_edit)
        main_layout.addWidget(buttons_box)
        dialog.setLayout(main_layout)
        DeleteDialogs.set_ui_text(dialog, delete_all_contacts_text_label, buttons_box, parent)
        return dialog

    @staticmethod
    def set_ui_text(dialog_widget: QDialog, label: QLabel, button_box: QDialogButtonBox, parent=None) -> None:
        ui_text = LanguageProvider.get_dialog_text(DeleteDialogs.class_name)
        widgets = [dialog_widget, label]
        widgets.extend(button_box.buttons())
        try:
            for widget in widgets:
                if widget.objectName() in ui_text:
                    if isinstance(widget, QDialog):
                        widget.setWindowTitle(ui_text[widget.objectName()])
                    elif isinstance(widget, (QLabel, QPushButton)):
                        widget.setText(ui_text[widget.objectName()])
        except Exception as e:
            ErrorHandler.exception_handler(e, parent)

    @staticmethod
    def delete_accepted(dialog: QDialog, label: QLabel, line_edit: QLineEdit):
        ui_text = LanguageProvider.get_dialog_text(DeleteDialogs.class_name)
        try:
            delete_word = ui_text[label.objectName()]
            if line_edit.text().strip().upper() == delete_word.split(":")[-1].strip().upper():
                dialog.accept()
        except Exception as e:
            ErrorHandler.exception_handler(e)