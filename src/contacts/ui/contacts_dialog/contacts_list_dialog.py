from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QLabel, QDialogButtonBox, QPushButton

from src.contacts.ui.contacts_dialog.dialog_widgets.duplicate_listwidget import DuplicateListWidget
from src.utilities.error_handler import ErrorHandler
from src.utilities.icon_provider import IconProvider
from src.utilities.language_provider import LanguageProvider


# noinspection PyTypeChecker,PyUnresolvedReferences
class ContactsListDialog(QDialog):
    def __init__(self, duplicate_contacts: list, mode: str, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("contactsListDialog")
        IconProvider.set_window_icon(self, "mainWindow")
        self.contacts_list = duplicate_contacts
        self.mode = mode
        self.setFixedSize(500, 400)
        self.setLayout(self.create_gui())
        button_box = self.findChild(QDialogButtonBox)
        if button_box:
            self.buttons = button_box.findChildren(QPushButton)
        self.set_ui_text()
        self.set_tooltips()
        self.result_code = None
        self.selected_id = None

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        duplicate_text_label = QLabel()
        duplicate_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        duplicate_text_label.setStyleSheet("font-size: 25px; font-family: Arial;")
        duplicate_text_label.setObjectName("duplicateTextLabel")
        self.duplicate_listwidget = DuplicateListWidget(self.contacts_list)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.RestoreDefaults | QDialogButtonBox.StandardButton.Ok
                                      | QDialogButtonBox.StandardButton.Cancel)
        continue_button = button_box.button(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(self.accept)
        show_contact_button = button_box.button(QDialogButtonBox.StandardButton.RestoreDefaults)
        show_contact_button.setObjectName("showContactButton")
        show_contact_button.clicked.connect(self.get_duplicate_contact_id)
        continue_button.setObjectName("continueButton")
        cancel_button = button_box.button(QDialogButtonBox.StandardButton.Cancel)
        cancel_button.setObjectName("cancelButton")
        cancel_button.clicked.connect(self.dialog_rejected)
        main_layout.addWidget(duplicate_text_label)
        main_layout.addWidget(self.duplicate_listwidget)
        main_layout.addWidget(button_box)
        return main_layout

    def set_ui_text(self) -> None:
        try:
            ui_text = LanguageProvider.get_dialog_text(self.objectName())
            widgets = self.findChildren(QLabel)
            if ui_text:
                for widget in widgets:
                    if widget.objectName() in ui_text:
                        if isinstance(widget, QLabel):
                            if self.mode == "context":
                                widget.setText(f"{ui_text.get(f"{widget.objectName()}Context", "")}\n{len(self.contacts_list)}")
                            else:
                                widget.setText(f"{ui_text.get(widget.objectName(), "")}\n{len(self.contacts_list)}")
                for button in self.buttons:
                    if button.objectName() in ui_text:
                        if isinstance(button, QPushButton):
                            if self.mode == "context":
                                if button.objectName() == "continueButton":
                                    button.hide()
                                    continue
                                else:
                                    button.setText(ui_text.get(button.objectName(), ""))
                            else:
                                button.setText(ui_text.get(button.objectName(), ""))
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_tooltips(self) -> None:
        try:
            tooltips_text = LanguageProvider.get_tooltips_text(self.objectName())
            for button in self.buttons:
                if isinstance(button, QPushButton):
                    if self.mode == "context":
                        if button.objectName() == "continueButton":
                            continue
                        else:
                            button.setToolTip(tooltips_text.get(f"{button.objectName()}Context", ""))
                    else:
                        button.setToolTip(tooltips_text.get(button.objectName(), ""))
                button.setToolTipDuration(5000)
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def dialog_rejected(self) -> str:
        self.result_code = "rejected"
        self.reject()
        return self.result_code

    def get_duplicate_contact_id(self) -> str:
        try:
            self.selected_id = self.duplicate_listwidget.return_selected_contact_id()
            self.result_code = "jump_to_contact"
            self.reject()
        except Exception as e:
            ErrorHandler.exception_handler(e, self)