from PyQt6.QtCore import QSize
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu

from src.utilities.error_handler import ErrorHandler
from src.utilities.icon_provider import IconProvider
from src.utilities.language_provider import LanguageProvider


class ContextMenu(QMenu):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("contextMenu")
        self.create_gui()
        self.widgets = self.findChildren((QMenu, QAction))
        self.set_ui_text()
        IconProvider.set_buttons_icon(self.objectName(), self.widgets, QSize(15, 15), self)

    def create_gui(self) -> None:
        add_contact_action = QAction("přidat", self)
        add_contact_action.setObjectName("addContactAction")
        update_contact_action = QAction("upravit", self)
        update_contact_action.setObjectName("updateContactAction")
        delete_contact_action = QAction("smazat", self)
        delete_contact_action.setObjectName("deleteContactAction")
        copy_menu = QMenu("kopírovat", self)
        copy_menu.setObjectName("copyMenu")
        copy_name_action = QAction("jméno", self)
        copy_name_action.setObjectName("copyNameAction")
        copy_email_action = QAction("email", self)
        copy_email_action.setObjectName("copyEmailAction")
        copy_phone_number_action = QAction("telefon", self)
        copy_phone_number_action.setObjectName("copyPhoneNumberAction")
        export_menu = QMenu("export", self)
        export_menu.setObjectName("exportMenu")
        export_csv_action = QAction("csv", self)
        export_csv_action.setObjectName("exportCsvAction")
        export_vcard_action = QAction("vcard", self)
        export_vcard_action.setObjectName("exportVcardAction")
        export_pdf_action = QAction("pdf", self)
        export_pdf_action.setObjectName("exportPdfAction")
        print_menu = QMenu("tisk", self)
        print_menu.setObjectName("printMenu")
        print_contact_action = QAction("tisk kontaktu", self)
        print_contact_action.setObjectName("printContactAction")
        print_contact_list_action = QAction("tisk seznamu", self)
        print_contact_list_action.setObjectName("printContactListAction")
        preview_menu = QMenu("náhled", self)
        preview_menu.setObjectName("previewMenu")
        preview_contact_action = QAction("náhled kontaktu", self)
        preview_contact_action.setObjectName("previewContactAction")
        preview_contact_list_action = QAction("náhled kontaktů", self)
        preview_contact_list_action.setObjectName("previewContactListAction")
        preview_qr_code_action = QAction("qr kód", self)
        preview_qr_code_action.setObjectName("previewQrCodeAction")
        contact_check_menu = QMenu("kontrola kontaktů", self)
        contact_check_menu.setObjectName("contactCheckMenu")
        contact_check_birthday_action = QAction("kontrola narození", self)
        contact_check_birthday_action.setObjectName("contactCheckBirthdayAction")
        contact_check_duplicity_action = QAction("hledat duplicity", self)
        contact_check_duplicity_action.setObjectName("contactCheckDuplicityAction")
        self.addActions([add_contact_action, update_contact_action, delete_contact_action])
        self.addSeparator()
        self.addMenu(copy_menu)
        copy_menu.addActions([copy_name_action, copy_email_action, copy_phone_number_action])
        self.addSeparator()
        self.addMenu(export_menu)
        export_menu.addActions([export_csv_action, export_vcard_action, export_pdf_action])
        self.addSeparator()
        self.addMenu(print_menu)
        print_menu.addActions([print_contact_action, print_contact_list_action])
        self.addSeparator()
        self.addMenu(preview_menu)
        preview_menu.addActions([preview_contact_action, preview_contact_list_action, preview_qr_code_action])
        self.addSeparator()
        self.addMenu(contact_check_menu)
        contact_check_menu.addActions([contact_check_birthday_action, contact_check_duplicity_action])

    def set_ui_text(self) -> None:
        try:
            ui_text = LanguageProvider.get_context_menu_text(self.objectName())
            for widget in self.widgets:
                if widget.objectName() in ui_text:
                    if isinstance(widget, QMenu):
                        widget.setTitle(ui_text[widget.objectName()])
                    elif isinstance(widget, QAction):
                        widget.setText(ui_text[widget.objectName()])
        except Exception as e:
            ErrorHandler.exception_handler(e, self)