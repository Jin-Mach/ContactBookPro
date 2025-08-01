import sys

from typing import TYPE_CHECKING

from PyQt6.QtCore import QSize, QModelIndex, Qt
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QWidget, QLayout, QHBoxLayout, QMainWindow, QComboBox

from src.contacts.controlers.advanced_search_controller import AdvancedSearchController
from src.contacts.controlers.completer_controller import CompleterController
from src.contacts.controlers.contact_search_controler import ContactSearchController
from src.contacts.controlers.contacts_controller import ContactsController
from src.contacts.controlers.filters_controller import FiltersController
from src.contacts.utilities.contact_validator import ContactValidator
from src.utilities.error_handler import ErrorHandler
from src.utilities.icon_provider import IconProvider
from src.utilities.language_provider import LanguageProvider

if TYPE_CHECKING:
    from src.database.models.mandatory_model import MandatoryModel
    from src.database.models.work_model import WorkModel
    from src.database.models.social_model import SocialModel
    from src.database.models.detail_model import DetailModel
    from src.database.models.info_model import InfoModel
    from src.contacts.ui.main_widgets.contacts_detail_widget import ContactsDetailWidget
    from src.contacts.ui.main_widgets.contacts_tableview_widget import ContactsTableviewWidget
    from src.contacts.ui.main_widgets.contacts_statusbar_widget import ContactsStatusbarWidget
    from src.database.models.completer_model import CompleterModel
    from src.map.controllers.map_controller import MapController
    from src.statistics.controllers.statistics_controller import StatisticsController


# noinspection PyUnresolvedReferences
class ContactsToolbarWidget(QWidget):
    def __init__(self, main_window: QMainWindow, db_connection: QSqlDatabase, mandatory_model: "MandatoryModel",
                 work_model: "WorkModel", social_model: "SocialModel", detail_model: "DetailModel", info_model: "InfoModel",
                 detail_widget: "ContactsDetailWidget", table_view: "ContactsTableviewWidget", contacts_statusbar: "ContactsStatusbarWidget",
                 completer_model: "CompleterModel", map_controller: "MapController", statistics_controller: "StatisticsController",
                 parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("contactsToolbarWidget")
        self.db_connection = db_connection
        self.mandatory_model = mandatory_model
        self.table_view = table_view
        self.completer_model = completer_model
        self.contacts_statusbar = contacts_statusbar
        self.map_controller = map_controller
        self.statistics_controller = statistics_controller
        self.buttons_size = QSize(35, 35)
        self.setLayout(self.create_gui())
        self.set_ui_text()
        self.set_tooltips_text()
        self.set_style()
        self.create_connection()
        self.create_shortcuts()
        self.contacts_controller = ContactsController(main_window, self.db_connection, self.mandatory_model, work_model,
                                                      social_model, detail_model, info_model, detail_widget, table_view,
                                                      self.contacts_statusbar, self.map_controller, self.statistics_controller,
                                                      self)
        self.completer_controller = CompleterController(self.completer_model, self.table_view, self.search_line_edit)
        self.completer_controller.setup()
        self.contact_search_controller = ContactSearchController(self.completer_controller, self.mandatory_model, table_view, self.contacts_statusbar, self.search_combobox, self)
        self.advanced_search_controller = AdvancedSearchController(self.db_connection, self.mandatory_model, self.contacts_statusbar, self)
        self.filters_controller = FiltersController(self.advanced_search_controller.dialog.search_mandatory_widget,
                                                    self.advanced_search_controller.dialog.search_non_mandatory_widget, self)
        IconProvider.set_buttons_icon(self.objectName(), self.findChildren(QPushButton), self.buttons_size, self)
        self.table_view.selectionModel().currentColumnChanged.connect(self.set_validator)

    def create_gui(self) -> QLayout:
        main_layout = QHBoxLayout()
        self.add_new_contact_pushbutton = QPushButton()
        self.add_new_contact_pushbutton.setObjectName("addNewContactPushbutton")
        self.add_new_contact_pushbutton.setFixedSize(self.buttons_size)
        self.update_contact_pushbutton = QPushButton()
        self.update_contact_pushbutton.setObjectName("updateContactPushbutton")
        self.update_contact_pushbutton.setFixedSize(self.buttons_size)
        self.delete_contact_pushbutton = QPushButton()
        self.delete_contact_pushbutton.setObjectName("deleteContactPushbutton")
        self.delete_contact_pushbutton.setFixedSize(self.buttons_size)
        self.delete_all_contacts_pushbutton = QPushButton()
        self.delete_all_contacts_pushbutton.setObjectName("deleteAllContactsPushbutton")
        self.delete_all_contacts_pushbutton.setFixedSize(self.buttons_size)
        self.search_text_label = QLabel()
        self.search_text_label.setObjectName("searchTextLabel")
        self.search_combobox = QComboBox()
        self.search_combobox.setObjectName("searchCombobox")
        self.search_combobox.setDisabled(True)
        self.search_combobox.setFixedWidth(300)
        self.search_combobox.hide()
        self.search_line_edit = QLineEdit()
        self.search_line_edit.setObjectName("searchLineEdit")
        self.search_line_edit.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.search_line_edit.setFixedSize(300, 35)
        self.search_line_edit.setDisabled(True)
        self.search_pushbutton = QPushButton()
        self.search_pushbutton.setObjectName("searchPushbutton")
        self.search_pushbutton.setFixedSize(self.buttons_size)
        self.advanced_search_pushbutton = QPushButton()
        self.advanced_search_pushbutton.setObjectName("advancedSearchPushbutton")
        self.advanced_search_pushbutton.setFixedSize(self.buttons_size)
        self.reset_filter_pushbutton = QPushButton()
        self.reset_filter_pushbutton.setObjectName("resetFilterPushbutton")
        self.reset_filter_pushbutton.setFixedSize(self.buttons_size)
        self.user_filters_pushbutton = QPushButton()
        self.user_filters_pushbutton.setObjectName("userFiltersPushbutton")
        self.user_filters_pushbutton.setFixedSize(self.buttons_size)
        main_layout.addWidget(self.add_new_contact_pushbutton)
        main_layout.addWidget(self.update_contact_pushbutton)
        main_layout.addWidget(self.delete_contact_pushbutton)
        main_layout.addWidget(self.delete_all_contacts_pushbutton)
        main_layout.addStretch()
        main_layout.addWidget(self.search_text_label)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.search_combobox)
        main_layout.addWidget(self.search_line_edit)
        main_layout.addWidget(self.search_pushbutton)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.advanced_search_pushbutton)
        main_layout.addWidget(self.reset_filter_pushbutton)
        main_layout.addWidget(self.user_filters_pushbutton)
        main_layout.addStretch()
        return main_layout

    def set_ui_text(self) -> None:
        try:
            ui_text = LanguageProvider.get_ui_text(self.objectName())
            widgets = self.findChildren((QLabel, QLineEdit))
            if ui_text:
                for widget in widgets:
                    if widget.objectName() in ui_text:
                        if isinstance(widget, QLabel):
                            widget.setText(ui_text.get(widget.objectName(), ""))
                        elif isinstance(widget, QLineEdit):
                            widget.setPlaceholderText(ui_text.get(widget.objectName(), ""))
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_tooltips_text(self) -> None:
        try:
            tooltips_text = LanguageProvider.get_tooltips_text(self.objectName())
            statustips_text = LanguageProvider.get_statustips_text(self.objectName())
            if sys.platform == "darwin":
                for key, value in statustips_text.items():
                    statustips_text[key] = value.replace("Ctrl", "Cmd")
            buttons = self.findChildren(QPushButton)
            for button in buttons:
                name = button.objectName()
                if name in tooltips_text:
                    button.setToolTip(tooltips_text.get(name, ""))
                if name in statustips_text:
                    button.setStatusTip(statustips_text.get(name, ""))
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_style(self) -> None:
        self.search_text_label.setStyleSheet("font-size: 12pt;")
        self.search_line_edit.setStyleSheet("font-size: 15pt;")

    def create_connection(self) -> None:
        self.add_new_contact_pushbutton.clicked.connect(self.add_new_contact)
        self.update_contact_pushbutton.clicked.connect(self.update_existing_contact)
        self.delete_contact_pushbutton.clicked.connect(self.delete_contact)
        self.delete_all_contacts_pushbutton.clicked.connect(self.delete_all_contacts)
        self.search_pushbutton.clicked.connect(self.search_contact)
        self.advanced_search_pushbutton.clicked.connect(self.advanced_search)
        self.reset_filter_pushbutton.clicked.connect(self.reset_filter)
        self.user_filters_pushbutton.clicked.connect(self.show_user_filters)

    def create_shortcuts(self) -> None:
        self.add_new_contact_shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        self.add_new_contact_shortcut.activated.connect(self.add_new_contact)
        self.update_contact_shortcut = QShortcut(QKeySequence("Ctrl+U"), self)
        self.update_contact_shortcut.activated.connect(self.update_existing_contact)
        self.delete_contact_shortcut = QShortcut(QKeySequence("Ctrl+D"), self)
        self.delete_contact_shortcut.activated.connect(self.delete_contact)
        self.delete_all_contacts_shortcut = QShortcut(QKeySequence("Ctrl+Shift+D"), self)
        self.delete_all_contacts_shortcut.activated.connect(self.delete_all_contacts)
        self.search_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        self.search_shortcut.activated.connect(self.search_contact)
        self.advanced_search_shortcut = QShortcut(QKeySequence("Ctrl+Shift+F"), self)
        self.advanced_search_shortcut.activated.connect(self.advanced_search)
        self.reset_filter_shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        self.reset_filter_shortcut.activated.connect(self.reset_filter)
        self.user_filters_shortcut = QShortcut(QKeySequence("Ctrl+L"), self)
        self.user_filters_shortcut.activated.connect(self.show_user_filters)

    def add_new_contact(self) -> None:
        try:
            self.contacts_controller.add_new_contact()
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def update_existing_contact(self) -> None:
        try:
            self.contacts_controller.update_contact()
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def delete_contact(self) -> None:
        try:
            self.contacts_controller.delete_contact()
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def delete_all_contacts(self) -> None:
        try:
            self.contacts_controller.delete_all_contacts()
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def search_contact(self) -> None:
        try:
            self.contact_search_controller.basic_search(self.search_line_edit)
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def advanced_search(self) -> None:
        self.advanced_search_controller.advanced_search()

    def reset_filter(self) -> None:
        try:
            self.contact_search_controller.reset_filter(self.search_line_edit)
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def show_user_filters(self) -> None:
        try:
            self.filters_controller.show_user_filters(self.db_connection, self.mandatory_model, self.contacts_statusbar)
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_validator(self, current: QModelIndex) -> None:
        try:
            column = current.column()
            text = self.search_line_edit.text().strip()
            if column in (4, 5):
                validator_function = ContactValidator.search_input_validator
                filter_function = ContactValidator.filter_invalid_characters
                if column == 4:
                    validator_function(email_edit=self.search_line_edit)
                    text = filter_function(self.search_line_edit)
                elif column == 5:
                    validator_function(phone_edit=self.search_line_edit)
                    text = filter_function(self.search_line_edit)
            else:
                self.search_line_edit.setValidator(None)
            self.search_line_edit.setText(text)
            self.search_line_edit.setFocus()
        except Exception as e:
            ErrorHandler.exception_handler(e, self)