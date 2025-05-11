from functools import partial

from PyQt6.QtCore import QSize, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QWidget, QLayout, QFormLayout, QLabel, QLineEdit, QComboBox, QHBoxLayout, QPushButton

from src.contacts.contacts_utilities.contact_validator import ContactValidator
from src.utilities.error_handler import ErrorHandler
from src.utilities.icon_provider import IconProvider
from src.utilities.language_provider import LanguageProvider


class SearchWorkWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("searchWorkWidget")
        self.operator_width = 150
        self.setLayout(self.create_gui())
        self.set_ui_text()
        ContactValidator.search_input_validator(email_edit=self.search_work_email_edit, phone_edit=self.search_work_phone_number_edit)

    def create_gui(self) -> QLayout:
        main_layout = QFormLayout()
        self.search_work_company_text_label = QLabel()
        self.search_work_company_text_label.setObjectName("searchWorkCompanyTextLabel")
        self.search_work_company_edit = QLineEdit()
        self.search_work_company_edit.setObjectName("searchWorkCompanyEdit")
        self.search_work_company_operator = QComboBox()
        self.search_work_company_operator.setObjectName("searchWorkCompanyOperator")
        self.search_work_company_operator.setFixedWidth(self.operator_width)
        self.search_work_email_text_label = QLabel()
        self.search_work_email_text_label.setObjectName("searchWorkEmailTextLabel")
        self.search_work_email_edit = QLineEdit()
        self.search_work_email_edit.setObjectName("searchWorkEmailEdit")
        self.search_work_email_operator = QComboBox()
        self.search_work_email_operator.setObjectName("searchWorkEmailOperator")
        self.search_work_email_operator.setFixedWidth(self.operator_width)
        self.search_work_phone_number_text_label = QLabel()
        self.search_work_phone_number_text_label.setObjectName("searchWorkPhoneNumberTextLabel")
        self.search_work_phone_number_edit = QLineEdit()
        self.search_work_phone_number_edit.setObjectName("searchWorkPhoneNumberEdit")
        self.search_work_phone_number_operator = QComboBox()
        self.search_work_phone_number_operator.setObjectName("searchPhoneNumberOperator")
        self.search_work_phone_number_operator.setFixedWidth(self.operator_width)
        self.search_work_city_text_label = QLabel()
        self.search_work_city_text_label.setObjectName("searchWorkCityTextLabel")
        self.search_work_city_edit = QLineEdit()
        self.search_work_city_edit.setObjectName("searchWorkCityEdit")
        self.search_work_city_operator = QComboBox()
        self.search_work_city_operator.setObjectName("searchWorkCityOperator")
        self.search_work_city_operator.setFixedWidth(self.operator_width)
        self.search_work_street_text_label = QLabel()
        self.search_work_street_text_label.setObjectName("searchWorkStreetTextLabel")
        self.search_work_street_edit = QLineEdit()
        self.search_work_street_edit.setObjectName("searchWorkStreetEdit")
        self.search_work_street_operator = QComboBox()
        self.search_work_street_operator.setObjectName("searchWorkStreetOperator")
        self.search_work_street_operator.setFixedWidth(self.operator_width)
        self.search_work_house_number_text_label = QLabel()
        self.search_work_house_number_text_label.setObjectName("searchWorkHouseNumberTextLabel")
        self.search_work_house_number_edit = QLineEdit()
        self.search_work_house_number_edit.setObjectName("searchWorkHouseNumberEdit")
        self.search_work_house_number_operator = QComboBox()
        self.search_work_house_number_operator.setObjectName("searchWorkHouseNumberOperator")
        self.search_work_house_number_operator.setFixedWidth(self.operator_width)
        self.search_work_post_code_text_label = QLabel()
        self.search_work_post_code_text_label.setObjectName("searchWorkPostCodeTextLabel")
        self.search_work_post_code_edit = QLineEdit()
        self.search_work_post_code_edit.setObjectName("searcWorkPostCodeEdit")
        self.search_work_post_code_operator = QComboBox()
        self.search_work_post_code_operator.setObjectName("searchWorkPostCodeOperator")
        self.search_work_post_code_operator.setFixedWidth(self.operator_width)
        self.search_work_country_text_label = QLabel()
        self.search_work_country_text_label.setObjectName("searchWorkCountryTextLabel")
        self.search_work_country_edit = QLineEdit()
        self.search_work_country_edit.setObjectName("searchWorkCountryEdit")
        self.search_work_country_operator = QComboBox()
        self.search_work_country_operator.setObjectName("searchWorkCountryOperator")
        self.search_work_country_operator.setFixedWidth(self.operator_width)
        fields = [
            (self.search_work_company_text_label, self.search_work_company_edit, self.search_work_company_operator),
            (self.search_work_email_text_label, self.search_work_email_edit, self.search_work_email_operator),
            (self.search_work_phone_number_text_label, self.search_work_phone_number_edit, self.search_work_phone_number_operator),
            (self.search_work_city_text_label, self.search_work_city_edit, self.search_work_city_operator),
            (self.search_work_street_text_label, self.search_work_street_edit, self.search_work_street_operator),
            (self.search_work_house_number_text_label, self.search_work_house_number_edit, self.search_work_house_number_operator),
            (self.search_work_post_code_text_label, self.search_work_post_code_edit, self.search_work_post_code_operator),
            (self.search_work_country_text_label, self.search_work_country_edit, self.search_work_country_operator)
        ]
        tooltip_text = LanguageProvider.get_tooltips_text("advancedSearchDialog")
        for label, edit, operator in fields:
            layout = QHBoxLayout()
            clear_filter_pushbutton = QPushButton()
            clear_filter_pushbutton.setObjectName("clearFilterPushbutton")
            IconProvider.set_buttons_icon("advancedSearchDialog", [clear_filter_pushbutton], QSize(25, 25))
            if clear_filter_pushbutton.objectName() in tooltip_text:
                clear_filter_pushbutton.setToolTip(tooltip_text[clear_filter_pushbutton.objectName()])
                clear_filter_pushbutton.setToolTipDuration(5000)
            clear_filter_pushbutton.clicked.connect(partial(SearchWorkWidget.reset_row_filter, edit, operator))
            layout.addWidget(edit)
            layout.addWidget(operator)
            layout.addWidget(clear_filter_pushbutton)
            main_layout.addRow(label, layout)
        return main_layout

    def set_ui_text(self) -> None:
        try:
            ui_text = LanguageProvider.get_search_dialog_text(self.objectName())
            widgets = self.findChildren((QLabel, QComboBox, QLineEdit))
            for widget in widgets:
                if isinstance(widget, QLabel):
                    if widget.objectName() in ui_text:
                        widget.setText(ui_text[widget.objectName()])
                elif isinstance(widget, QComboBox):
                    if "operators" in ui_text:
                        widget.addItems(ui_text["operators"])
                elif isinstance(widget, QLineEdit):
                    if widget.objectName() in ui_text:
                        widget.setPlaceholderText(ui_text[widget.objectName()])
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    @staticmethod
    def reset_row_filter(edit: QLineEdit, operator: QComboBox) -> None:
        edit.clear()
        operator.setCurrentIndex(0)

    def reset_all_filters(self) -> None:
        widgets = self.findChildren((QComboBox, QLineEdit))
        for widget in widgets:
            if isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)
            else:
                widget.clear()