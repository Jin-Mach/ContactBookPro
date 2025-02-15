import pathlib

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QTabWidget, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QFormLayout

from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class TabInfoWidget(QTabWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("tabInfoWidget")
        self.parent = parent
        self.setFixedHeight(250)
        self.setContentsMargins(0, 0, 0, 0)
        self.buttons_size = QSize(35, 35)
        self.addTab(self.create_personal_tab(), "")
        self.addTab(self.create_work_tab(), "")
        self.set_ui_text()
        self.set_icons()

    def create_personal_tab(self) -> QWidget:
        personal_widget = QWidget()
        personal_layout = QVBoxLayout()
        personal_social_network_layout = QHBoxLayout()
        self.facebook_pushbutton = QPushButton()
        self.facebook_pushbutton.setObjectName("facebookPushbutton")
        self.facebook_pushbutton.setFixedSize(self.buttons_size)
        self.x_pushbutton = QPushButton()
        self.x_pushbutton.setObjectName("xPushbutton")
        self.x_pushbutton.setFixedSize(self.buttons_size)
        self.instagram_pushbutton = QPushButton()
        self.instagram_pushbutton.setObjectName("instagramPushbutton")
        self.instagram_pushbutton.setFixedSize(self.buttons_size)
        personal_social_network_layout.addWidget(self.facebook_pushbutton)
        personal_social_network_layout.addWidget(self.x_pushbutton)
        personal_social_network_layout.addWidget(self.instagram_pushbutton)
        personal_social_network_layout.addStretch()
        personal_contact_layout = QFormLayout()
        self.personal_email_text_label = QLabel()
        self.personal_email_text_label.setObjectName("personalEmailTextLabel")
        self.personal_email_label = QLabel("personal@email.com")
        self.personal_email_label.setObjectName("personalEmailLabel")
        self.personal_phone_number_text_label = QLabel()
        self.personal_phone_number_text_label.setObjectName("personalPhoneNumberTextLabel")
        self.personal_phone_number_label = QLabel("123456789")
        self.personal_phone_number_label.setObjectName("personalPhoneNumberLabel")
        self.personal_address_text_label = QLabel()
        self.personal_address_text_label.setObjectName("personalAddressTextLabel")
        self.personal_address_label = QLabel("personal home 123")
        self.personal_address_label.setObjectName("personalAddressLabel")
        self.personal_city_text_label = QLabel()
        self.personal_city_text_label.setObjectName("personalCityTextLabel")
        self.personal_city_label = QLabel("personal city")
        self.personal_city_label.setObjectName("personalCityLabel")
        self.personal_post_code_text_label = QLabel()
        self.personal_post_code_text_label.setObjectName("personalPostCodeTextLabel")
        self.personal_post_code_label = QLabel("12345")
        self.personal_post_code_label.setObjectName("personalPostCodeLabel")
        self.personal_country_text_label = QLabel()
        self.personal_country_text_label.setObjectName("personalCountryTextLabel")
        self.personal_country_label = QLabel("personal country")
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
        self.github_pushbutton = QPushButton()
        self.github_pushbutton.setObjectName("githubPushbutton")
        self.github_pushbutton.setFixedSize(self.buttons_size)
        self.work_website_pushbutton = QPushButton()
        self.work_website_pushbutton.setObjectName("workWebsitePushbutton")
        self.work_website_pushbutton.setFixedSize(self.buttons_size)
        work_social_network_layout.addWidget(self.linkedin_pushbutton)
        work_social_network_layout.addWidget(self.github_pushbutton)
        work_social_network_layout.addWidget(self.work_website_pushbutton)
        work_social_network_layout.addStretch()
        work_contact_layout = QFormLayout()
        self.work_email_text_label = QLabel()
        self.work_email_text_label.setObjectName("workEmailTextLabel")
        self.work_email_label = QLabel("work@email.com")
        self.work_email_label.setObjectName("workEmailLabel")
        self.work_phone_number_text_label = QLabel()
        self.work_phone_number_text_label.setObjectName("workPhoneNumberTextLabel")
        self.work_phone_number_label = QLabel("987654321")
        self.work_phone_number_label.setObjectName("workPhoneNumberLabel")
        self.work_address_text_label = QLabel()
        self.work_address_text_label.setObjectName("workAddressTextLabel")
        self.work_address_label = QLabel("work home 123")
        self.work_address_label.setObjectName("workAddressLabel")
        self.work_city_text_label = QLabel()
        self.work_city_text_label.setObjectName("workCityTextLabel")
        self.work_city_label = QLabel("work city")
        self.work_city_label.setObjectName("workCityLabel")
        self.work_post_code_text_label = QLabel()
        self.work_post_code_text_label.setObjectName("workPostCodeTextLabel")
        self.work_post_code_label = QLabel("54321")
        self.work_post_code_label.setObjectName("workPostCodeLabel")
        self.work_country_text_label = QLabel()
        self.work_country_text_label.setObjectName("workCountryTextLabel")
        self.work_country_label = QLabel("work country")
        self.work_country_label.setObjectName("workCountryLabel")
        work_widgets = [
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
        ui_text = LanguageProvider.get_ui_text(self.objectName())
        tab_text = ["personalTabText", "workTabText"]
        try:
            for index, text in enumerate(tab_text):
                if text in ui_text:
                    self.setTabText(index, ui_text[text])
            widgets = [self.personal_email_text_label, self.personal_phone_number_text_label, self.personal_address_text_label,
                       self.personal_city_text_label, self.personal_post_code_text_label, self.personal_country_text_label,
                       self.work_email_text_label, self.work_phone_number_text_label, self.work_address_text_label,
                       self.work_city_text_label, self.work_post_code_text_label, self.work_country_text_label]
            for widget in widgets:
                if widget.objectName() in ui_text:
                    widget.setText(ui_text[widget.objectName()])
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def set_icons(self) -> None:
        icons_path = pathlib.Path(__file__).parent.parent.parent.parent.joinpath("icons", "social_networks_icons")
        buttons = {
            self.facebook_pushbutton: "facebook_icon.png",
            self.x_pushbutton: "x_icon.png",
            self.instagram_pushbutton: "instagram_icon.png",
            self.linkedin_pushbutton: "linkedin_icon.png",
            self.github_pushbutton: "github_icon.png",
            self.work_website_pushbutton: "work_website_icon.png",
        }
        try:
            for button, icon_file in buttons.items():
                icon_path = icons_path.joinpath(icon_file)
                button.setIcon(QIcon(str(icon_path)))
                button.setIconSize(QSize(30, 30))
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)