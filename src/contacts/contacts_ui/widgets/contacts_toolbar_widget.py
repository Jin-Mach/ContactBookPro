from PyQt6.QtCore import QSize
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QWidget, QLayout, QHBoxLayout, QMainWindow

from src.contacts.contacts_ui.widgets.contacts_detail_widget import ContactsDetailWidget
from src.contacts.contacts_ui.widgets.contacts_statusbar_widget import ContactsStatusbarWidget
from src.contacts.contacts_ui.widgets.contacts_tableview_widget import ContactsTableviewWidget
from src.controlers.contacts_controller import ContactsController
from src.database.models.detail_model import DetailModel
from src.database.models.info_model import InfoModel
from src.database.models.mandatory_model import MandatoryModel
from src.database.models.social_model import SocialModel
from src.database.models.work_model import WorkModel
from src.utilities.error_handler import ErrorHandler
from src.utilities.icon_provider import IconProvider
from src.utilities.language_provider import LanguageProvider


# noinspection PyUnresolvedReferences
class ContactsToolbarWidget(QWidget):
    def __init__(self, main_window: QMainWindow, mandatory_model: MandatoryModel, work_model: WorkModel, social_model: SocialModel, detail_model: DetailModel,
                 info_model: InfoModel, detail_widget: ContactsDetailWidget, table_view: ContactsTableviewWidget,
                 status_bar: ContactsStatusbarWidget, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("contactsToolbarWidget")
        self.table_view = table_view
        self.contacts_controler = ContactsController(main_window, mandatory_model, work_model, social_model, detail_model, info_model,
                                                     detail_widget, table_view, status_bar, self)
        self.buttons_size = QSize(35, 35)
        self.setLayout(self.create_gui())
        self.set_ui_text()
        self.set_tooltips_text()
        IconProvider.set_buttons_icon(self.objectName(), self.findChildren(QPushButton), self.buttons_size, self)

    def create_gui(self) -> QLayout:
        main_layout = QHBoxLayout()
        self.add_new_contact_pushbutton = QPushButton()
        self.add_new_contact_pushbutton.setObjectName("addNewContactPushbutton")
        self.add_new_contact_pushbutton.setFixedSize(self.buttons_size)
        self.add_new_contact_pushbutton.clicked.connect(self.add_new_contact)
        self.update_contact_pushbutton = QPushButton()
        self.update_contact_pushbutton.setObjectName("updateContactPushbutton")
        self.update_contact_pushbutton.setFixedSize(self.buttons_size)
        self.update_contact_pushbutton.clicked.connect(self.update_existing_contact)
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
        widgets = self.findChildren((QLabel, QLineEdit))
        try:
            for widget in widgets:
                if widget.objectName() in ui_text:
                    if isinstance(widget, QLabel):
                        widget.setText(ui_text[widget.objectName()])
                    elif isinstance(widget, QLineEdit):
                        widget.setPlaceholderText(ui_text[widget.objectName()])
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_tooltips_text(self) -> None:
        tooltips_text = LanguageProvider.get_tooltips_text(self.objectName())
        buttons = self.findChildren(QPushButton)
        try:
            for button in buttons:
                if button.objectName() in tooltips_text:
                    button.setToolTip(tooltips_text[button.objectName()])
                    button.setToolTipDuration(5000)
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def add_new_contact(self) -> None:
        try:
            self.contacts_controler.add_new_contact()
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def update_existing_contact(self) -> None:
        try:
            if self.table_view.selectionModel().hasSelection():
                self.contacts_controler.update_contact()
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def delete_contact(self) -> None:
        try:
            if self.table_view.selectionModel().hasSelection():
                self.contacts_controler.delete_contact()
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def delete_all_contacts(self) -> None:
        try:
            self.contacts_controler.delete_all_contacts()
        except Exception as e:
            ErrorHandler.exception_handler(e, self)