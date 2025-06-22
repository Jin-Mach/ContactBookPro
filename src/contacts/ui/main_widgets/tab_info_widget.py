from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QTabWidget, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QFormLayout

from src.contacts.utilities.phone_utilities import format_phone_number
from src.contacts.utilities.url_utilities import open_url, update_buttons_state
from src.utilities.error_handler import ErrorHandler
from src.utilities.icon_provider import IconProvider
from src.utilities.language_provider import LanguageProvider


# noinspection PyUnresolvedReferences
class TabInfoWidget(QTabWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("tabInfoWidget")
        self.setFixedWidth(400)
        self.setContentsMargins(0, 0, 0, 0)
        self.buttons_size = QSize(35, 35)
        self.addTab(self.create_personal_tab(), "")
        self.addTab(self.create_work_tab(), "")
        self.set_ui_text()
        self.set_tooltips_text()
        IconProvider.set_buttons_icon(self.objectName(), self.findChildren(QPushButton), self.buttons_size, self)
        self.buttons = [self.facebook_pushbutton, self.x_pushbutton, self.instagram_pushbutton,
                        self.linkedin_pushbutton, self.github_pushbutton, self.work_website_pushbutton]
        self.create_connection()

    def create_personal_tab(self) -> QWidget:
        personal_widget = QWidget()
        personal_layout = QVBoxLayout()
        personal_social_network_layout = QHBoxLayout()
        self.facebook_pushbutton = QPushButton()
        self.facebook_pushbutton.setObjectName("facebookPushbutton")
        self.facebook_pushbutton.setFixedSize(self.buttons_size)
        self.facebook_pushbutton.setDisabled(True)
        self.x_pushbutton = QPushButton()
        self.x_pushbutton.setObjectName("xPushbutton")
        self.x_pushbutton.setFixedSize(self.buttons_size)
        self.x_pushbutton.setDisabled(True)
        self.instagram_pushbutton = QPushButton()
        self.instagram_pushbutton.setObjectName("instagramPushbutton")
        self.instagram_pushbutton.setFixedSize(self.buttons_size)
        self.instagram_pushbutton.setDisabled(True)
        personal_social_network_layout.addWidget(self.facebook_pushbutton)
        personal_social_network_layout.addWidget(self.x_pushbutton)
        personal_social_network_layout.addWidget(self.instagram_pushbutton)
        personal_social_network_layout.addStretch()
        personal_contact_layout = QFormLayout()
        self.personal_email_text_label = QLabel()
        self.personal_email_text_label.setObjectName("personalEmailTextLabel")
        self.personal_email_label = QLabel()
        self.personal_email_label.setObjectName("personalEmailLabel")
        self.personal_phone_number_text_label = QLabel()
        self.personal_phone_number_text_label.setObjectName("personalPhoneNumberTextLabel")
        self.personal_phone_number_label = QLabel()
        self.personal_phone_number_label.setObjectName("personalPhoneNumberLabel")
        self.personal_address_text_label = QLabel()
        self.personal_address_text_label.setObjectName("personalAddressTextLabel")
        self.personal_address_label = QLabel()
        self.personal_address_label.setObjectName("personalAddressLabel")
        self.personal_city_text_label = QLabel()
        self.personal_city_text_label.setObjectName("personalCityTextLabel")
        self.personal_city_label = QLabel()
        self.personal_city_label.setObjectName("personalCityLabel")
        self.personal_post_code_text_label = QLabel()
        self.personal_post_code_text_label.setObjectName("personalPostCodeTextLabel")
        self.personal_post_code_label = QLabel()
        self.personal_post_code_label.setObjectName("personalPostCodeLabel")
        self.personal_country_text_label = QLabel()
        self.personal_country_text_label.setObjectName("personalCountryTextLabel")
        self.personal_country_label = QLabel()
        self.personal_country_label.setObjectName("personalCountryLabel")
        personal_widgets = [
            (self.personal_email_text_label, self.personal_email_label),
            (self.personal_phone_number_text_label, self.personal_phone_number_label),
            (self.personal_address_text_label, self.personal_address_label),
            (self.personal_city_text_label, self.personal_city_label),
            (self.personal_post_code_text_label, self.personal_post_code_label),
            (self.personal_country_text_label, self.personal_country_label),
        ]
        for label, edit in personal_widgets:
            personal_contact_layout.addRow(label, edit)
        personal_layout.addLayout(personal_social_network_layout)
        personal_layout.addLayout(personal_contact_layout)
        personal_layout.addStretch()
        personal_widget.setLayout(personal_layout)
        return personal_widget

    def create_work_tab(self) -> QWidget:
        work_widget = QWidget()
        work_layout = QVBoxLayout()
        work_social_network_layout = QHBoxLayout()
        self.linkedin_pushbutton = QPushButton()
        self.linkedin_pushbutton.setObjectName("linkedinPushbutton")
        self.linkedin_pushbutton.setFixedSize(self.buttons_size)
        self.linkedin_pushbutton.setDisabled(True)
        self.github_pushbutton = QPushButton()
        self.github_pushbutton.setObjectName("githubPushbutton")
        self.github_pushbutton.setFixedSize(self.buttons_size)
        self.github_pushbutton.setDisabled(True)
        self.work_website_pushbutton = QPushButton()
        self.work_website_pushbutton.setObjectName("websitePushbutton")
        self.work_website_pushbutton.setFixedSize(self.buttons_size)
        self.work_website_pushbutton.setDisabled(True)
        work_social_network_layout.addWidget(self.linkedin_pushbutton)
        work_social_network_layout.addWidget(self.github_pushbutton)
        work_social_network_layout.addWidget(self.work_website_pushbutton)
        work_social_network_layout.addStretch()
        work_contact_layout = QFormLayout()
        self.work_company_name_text_label = QLabel()
        self.work_company_name_text_label.setObjectName("workCompanyNameTextLabel")
        self.work_company_name_label = QLabel()
        self.work_company_name_label.setObjectName("workCompanyLabel")
        self.work_email_text_label = QLabel()
        self.work_email_text_label.setObjectName("workEmailTextLabel")
        self.work_email_label = QLabel()
        self.work_email_label.setObjectName("workEmailLabel")
        self.work_phone_number_text_label = QLabel()
        self.work_phone_number_text_label.setObjectName("workPhoneNumberTextLabel")
        self.work_phone_number_label = QLabel()
        self.work_phone_number_label.setObjectName("workPhoneNumberLabel")
        self.work_city_text_label = QLabel()
        self.work_city_text_label.setObjectName("workCityTextLabel")
        self.work_city_label = QLabel()
        self.work_city_label.setObjectName("workCityLabel")
        self.work_address_text_label = QLabel()
        self.work_address_text_label.setObjectName("workAddressTextLabel")
        self.work_address_label = QLabel()
        self.work_address_label.setObjectName("workAddressLabel")
        self.work_city_text_label = QLabel()
        self.work_city_text_label.setObjectName("workCityTextLabel")
        self.work_city_label = QLabel()
        self.work_city_label.setObjectName("workCityLabel")
        self.work_post_code_text_label = QLabel()
        self.work_post_code_text_label.setObjectName("workPostCodeTextLabel")
        self.work_post_code_label = QLabel()
        self.work_post_code_label.setObjectName("workPostCodeLabel")
        self.work_country_text_label = QLabel()
        self.work_country_text_label.setObjectName("workCountryTextLabel")
        self.work_country_label = QLabel()
        self.work_country_label.setObjectName("workCountryLabel")
        work_widgets = [
            (self.work_company_name_text_label, self.work_company_name_label),
            (self.work_email_text_label, self.work_email_label),
            (self.work_phone_number_text_label, self.work_phone_number_label),
            (self.work_address_text_label, self.work_address_label),
            (self.work_city_text_label, self.work_city_label),
            (self.work_post_code_text_label, self.work_post_code_label),
            (self.work_country_text_label, self.work_country_label),
        ]
        for text_label, label in work_widgets:
            work_contact_layout.addRow(text_label, label)
        work_layout.addLayout(work_social_network_layout)
        work_layout.addLayout(work_contact_layout)
        work_layout.addStretch()
        work_widget.setLayout(work_layout)
        return work_widget

    def set_ui_text(self) -> None:
        try:
            ui_text = LanguageProvider.get_ui_text(self.objectName())
            tab_text = ["personalTabText", "workTabText"]
            if ui_text:
                for index, text in enumerate(tab_text):
                    if text in ui_text:
                        self.setTabText(index, ui_text.get(text, ""))
                widgets = self.findChildren(QLabel)
                for widget in widgets:
                    if widget.objectName() in ui_text:
                        widget.setText(ui_text.get(widget.objectName(), ""))
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_tooltips_text(self) -> None:
        try:
            tooltips_text = LanguageProvider.get_tooltips_text(self.objectName())
            buttons = self.findChildren(QPushButton)
            if tooltips_text:
                for button in buttons:
                    if button.objectName() in tooltips_text:
                        button.setToolTip(tooltips_text.get(button.objectName(), ""))
                        button.setToolTipDuration(5000)
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def create_connection(self) -> None:
        self.facebook_pushbutton.clicked.connect(lambda: open_url(self.facebook_url))
        self.x_pushbutton.clicked.connect(lambda: open_url(self.x_url))
        self.instagram_pushbutton.clicked.connect(lambda: open_url(self.instagram_url))
        self.linkedin_pushbutton.clicked.connect(lambda: open_url(self.linkedin_url))
        self.github_pushbutton.clicked.connect(lambda: open_url(self.github_url))
        self.work_website_pushbutton.clicked.connect(lambda: open_url(self.website_url))

    def set_data(self, data: dict) -> None:
        try:
            self.facebook_url = data.get("facebook_url", "")
            self.x_url = data.get("x_url", "")
            self.instagram_url = data.get("instagram_url", "")
            self.personal_email_label.setText(data.get("personal_email", ""))
            self.personal_phone_number_label.setText(format_phone_number(data.get("personal_phone_number", "")))
            self.personal_address_label.setText(self.validate_address(
                data.get("personal_street", ""),
                data.get("personal_house_number", ""),
                data.get("personal_city", "")
            ))
            self.personal_city_label.setText(data.get("personal_city", ""))
            self.personal_post_code_label.setText(data.get("personal_post_code", ""))
            self.personal_country_label.setText(data.get("personal_country", ""))
            self.linkedin_url = data.get("linkedin_url", "")
            self.github_url = data.get("github_url", "")
            self.website_url = data.get("website_url", "")
            self.work_company_name_label.setText(data.get("company_name", ""))
            self.work_email_label.setText(data.get("work_email", ""))
            self.work_phone_number_label.setText(format_phone_number(data.get("personal_phone_number", "")))
            self.work_address_label.setText(self.validate_address(
                data.get("work_street", ""),
                data.get("work_house_number", ""),
                data.get("work_city", "")
            ))
            self.work_city_label.setText(data.get("work_city", ""))
            self.work_post_code_label.setText(data.get("work_post_code", ""))
            self.work_country_label.setText(data.get("work_country", ""))
            self.urls = [
                self.facebook_url, self.x_url, self.instagram_url,
                self.linkedin_url, self.github_url, self.website_url
            ]
            update_buttons_state(self.buttons, self.urls)
            self.setCurrentIndex(0)
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def reset_data(self) -> None:
        labels = self.findChildren(QLabel)
        for label in labels:
            if not label.objectName().endswith("TextLabel"):
                label.clear()
        for button in self.buttons:
            button.setDisabled(True)

    @staticmethod
    def validate_address(street: str, house_number: str, city: str) -> str:
        if not street:
            return f"{city} {house_number}"
        return f"{street} {house_number}"