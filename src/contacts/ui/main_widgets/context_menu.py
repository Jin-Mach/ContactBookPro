from PyQt6.QtCore import QSize
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu, QMainWindow, QTableView

from src.contacts.controlers.export_controlers.clipboard_export_controler import copy_to_clipboard
from src.contacts.controlers.export_controlers.csv_export_controler import CsvExportController
from src.contacts.controlers.export_controlers.excel_export_controler import ExcelExportController
from src.contacts.controlers.export_controlers.pdf_export_controller import PdfExportController
from src.contacts.controlers.export_controlers.qr_code_controler import qr_code_preview
from src.contacts.controlers.export_controlers.vcard_export_controler import export_to_vcard
from src.utilities.error_handler import ErrorHandler
from src.utilities.icon_provider import IconProvider
from src.utilities.language_provider import LanguageProvider


# noinspection PyUnresolvedReferences
class ContextMenu(QMenu):
    def __init__(self, contacts_controller: "ContactsController | None", csv_export_controller: CsvExportController | None,
                 excel_export_controller: ExcelExportController, pdf_export_controller: PdfExportController, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("contextMenu")
        self.parent = parent
        self.contacts_controller = contacts_controller
        self.csv_export_controller = csv_export_controller
        self.excel_export_controller = excel_export_controller
        self.pdf_export_controller = pdf_export_controller
        self.create_gui()
        self.widgets = self.findChildren((QMenu, QAction))
        self.set_ui_text()
        IconProvider.set_buttons_icon(self.objectName(), self.widgets, QSize(15, 15), self)

    def create_gui(self) -> None:
        self.add_contact_action = QAction(self)
        self.add_contact_action.setObjectName("addContactAction")
        self.update_contact_action = QAction(self)
        self.update_contact_action.setObjectName("updateContactAction")
        self.delete_contact_action = QAction(self)
        self.delete_contact_action.setObjectName("deleteContactAction")
        copy_menu = QMenu(self)
        copy_menu.setObjectName("copyMenu")
        self.copy_name_action = QAction(self)
        self.copy_name_action.setObjectName("copyNameAction")
        self.copy_email_action = QAction(self)
        self.copy_email_action.setObjectName("copyEmailAction")
        self.copy_phone_number_action = QAction(self)
        self.copy_phone_number_action.setObjectName("copyPhoneNumberAction")
        export_menu = QMenu(self)
        export_menu.setObjectName("exportMenu")
        export_csv_menu = QMenu(self)
        export_csv_menu.setObjectName("exportCsvMenu")
        self.export_filtered_data_csv_action = QAction(self)
        self.export_filtered_data_csv_action.setObjectName("exportFilteredDataCsvAction")
        self.export_all_data_csv_action = QAction(self)
        self.export_all_data_csv_action.setObjectName("exportAllDataCsvAction")
        export_excel_menu = QMenu(self)
        export_excel_menu.setObjectName("exportExcelMenu")
        self.export_filtered_data_excel_action = QAction(self)
        self.export_filtered_data_excel_action.setObjectName("exportFilteredDataExcelAction")
        self.export_all_data_excel_action = QAction(self)
        self.export_all_data_excel_action.setObjectName("exportAllDataExcelAction")
        self.export_vcard_action = QAction(self)
        self.export_vcard_action.setObjectName("exportVcardAction")
        print_menu = QMenu(self)
        print_menu.setObjectName("printMenu")
        self.print_contact_action = QAction(self)
        self.print_contact_action.setObjectName("printContactAction")
        self.print_contact_list_action = QAction(self)
        self.print_contact_list_action.setObjectName("printContactListAction")
        preview_menu = QMenu(self)
        preview_menu.setObjectName("previewMenu")
        self.preview_contact_action = QAction(self)
        self.preview_contact_action.setObjectName("previewContactAction")
        preview_contacts_list_menu = QMenu(self)
        preview_contacts_list_menu.setObjectName("previewContactsListMenu")
        self.preview_filtered_contacts_list_action = QAction(self)
        self.preview_filtered_contacts_list_action.setObjectName("previewFilteredContactsListAction")
        self.preview_all_contacts_list_action = QAction(self)
        self.preview_all_contacts_list_action.setObjectName("previewAllContactsListAction")
        self.preview_qr_code_action = QAction(self)
        self.preview_qr_code_action.setObjectName("previewQrCodeAction")
        contact_check_menu = QMenu(self)
        contact_check_menu.setObjectName("contactCheckMenu")
        self.contact_check_birthday_action = QAction(self)
        self.contact_check_birthday_action.setObjectName("contactCheckBirthdayAction")
        self.contact_check_duplicity_action = QAction(self)
        self.contact_check_duplicity_action.setObjectName("contactCheckDuplicityAction")
        self.addActions([self.add_contact_action, self.update_contact_action, self.delete_contact_action])
        self.addSeparator()
        self.addMenu(copy_menu)
        copy_menu.addActions([self.copy_name_action, self.copy_email_action, self.copy_phone_number_action])
        self.addSeparator()
        self.addMenu(export_menu)
        export_menu.addMenu(export_csv_menu)
        export_csv_menu.addActions([self.export_filtered_data_csv_action, self.export_all_data_csv_action])
        export_menu.addMenu(export_excel_menu)
        export_excel_menu.addActions([self.export_filtered_data_excel_action, self.export_all_data_excel_action])
        export_menu.addAction(self.export_vcard_action)
        self.addSeparator()
        self.addMenu(print_menu)
        print_menu.addActions([self.print_contact_action, self.print_contact_list_action])
        self.addSeparator()
        self.addMenu(preview_menu)
        preview_menu.addAction(self.preview_contact_action)
        preview_menu.addMenu(preview_contacts_list_menu)
        preview_contacts_list_menu.addActions([self.preview_filtered_contacts_list_action, self.preview_all_contacts_list_action])
        preview_menu.addAction(self.preview_qr_code_action)
        self.addSeparator()
        self.addMenu(contact_check_menu)
        contact_check_menu.addActions([self.contact_check_birthday_action, self.contact_check_duplicity_action])

    def set_ui_text(self) -> None:
        try:
            ui_text = LanguageProvider.get_context_menu_text(self.objectName())
            if ui_text:
                for widget in self.widgets:
                    if widget.objectName() in ui_text:
                        if isinstance(widget, QMenu):
                            widget.setTitle(ui_text.get(widget.objectName(), ""))
                        elif isinstance(widget, QAction):
                            widget.setText(ui_text.get(widget.objectName(), ""))
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def create_connection(self) -> None:
        connections = [(self.add_contact_action, self.contacts_controller.add_new_contact),
                       (self.update_contact_action, self.contacts_controller.update_contact),
                       (self.delete_contact_action, self.contacts_controller.delete_contact),
                       (self.copy_name_action, lambda: copy_to_clipboard(self.csv_export_controller.db_connection,
                                                                         self.index, "name", self.main_window)),
                       (self.copy_email_action, lambda: copy_to_clipboard(self.csv_export_controller.db_connection,
                                                                          self.index, "email", self.main_window)),
                       (self.copy_phone_number_action, lambda: copy_to_clipboard(self.csv_export_controller.db_connection,
                                                                                 self.index, "phone", self.main_window)),
                       (self.export_filtered_data_csv_action, lambda: self.csv_export_controller.export_filtered_to_csv(self.main_window)),
                       (self.export_all_data_csv_action, lambda: self.csv_export_controller.export_all_to_csv(self.main_window)),
                       (self.export_filtered_data_excel_action, lambda: self.excel_export_controller.export_filtered_to_excel(self.main_window)),
                       (self.export_all_data_excel_action, lambda: self.excel_export_controller.export_all_to_excel(self.main_window)),
                       (self.export_vcard_action, lambda: export_to_vcard(self.csv_export_controller.db_connection, self.index, self.main_window)),
                       (self.preview_qr_code_action, lambda: qr_code_preview(self.csv_export_controller.db_connection, self.index, self.main_window)),
                       (self.preview_filtered_contacts_list_action, lambda: self.pdf_export_controller.export_filtered_list_to_pdf(self.main_window)),
                       (self.preview_all_contacts_list_action, lambda: self.pdf_export_controller.export_all_list_to_pdf(self.main_window))]
        try:
            for action, method in connections:
                if isinstance(action, QAction):
                    action.triggered.disconnect()
                    action.triggered.connect(method)
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def set_context(self, main_window: QMainWindow, tableview: QTableView, index: int) -> None:
        self.main_window = main_window
        self.tableview = tableview
        self.index = index