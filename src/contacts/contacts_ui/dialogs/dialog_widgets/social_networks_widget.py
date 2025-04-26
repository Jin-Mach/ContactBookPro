from typing import Optional

from PyQt6.QtWidgets import QWidget, QLayout, QFormLayout, QLabel, QLineEdit, QTabWidget

from src.contacts.contacts_utilities.contact_validator import ContactValidator
from src.utilities.dialogs_provider import DialogsProvider
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class SocialNetworkWidget(QWidget):
    def __init__(self, main_tab: QTabWidget, non_mandatory_tab: QTabWidget, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("dialogSocialNetworkWidget")
        self.main_tab = main_tab
        self.non_mandatory_tab = non_mandatory_tab
        self.setLayout(self.create_gui())
        self.set_ui_text()

    def create_gui(self) -> QLayout:
        main_layout = QFormLayout()
        self.dialog_facebook_url_text_label = QLabel()
        self.dialog_facebook_url_text_label.setObjectName("dialogFacebookUrlTextLabel")
        self.dialog_facebook_url_edit = QLineEdit()
        self.dialog_facebook_url_edit.setObjectName("dialogFacebookUrlEdit")
        self.dialog_x_url_text_label = QLabel()
        self.dialog_x_url_text_label.setObjectName("dialogXUrlTextLabel")
        self.dialog_x_url_edit = QLineEdit()
        self.dialog_x_url_edit.setObjectName("dialogXUrlEdit")
        self.dialog_instagram_url_text_label = QLabel()
        self.dialog_instagram_url_text_label.setObjectName("dialogInstagramUrlTextLabel")
        self.dialog_instagram_url_edit = QLineEdit()
        self.dialog_instagram_url_edit.setObjectName("dialogInstagramUrlEdit")
        self.dialog_linkedin_url_text_label = QLabel()
        self.dialog_linkedin_url_text_label.setObjectName("dialogLinkedinUrlTextLabel")
        self.dialog_linkedin_url_edit = QLineEdit()
        self.dialog_linkedin_url_edit.setObjectName("dialogLinkedinUrlEdit")
        self.dialog_github_url_text_label = QLabel()
        self.dialog_github_url_text_label.setObjectName("dialogGithubUrlTextLabel")
        self.dialog_github_url_edit = QLineEdit()
        self.dialog_github_url_edit.setObjectName("dialogGithubUrlEdit")
        self.dialog_website_text_label = QLabel()
        self.dialog_website_text_label.setObjectName("dialogWebsiteUrlTextLabel")
        self.dialog_website_edit = QLineEdit()
        self.dialog_website_edit.setObjectName("dialogWebsiteUrlEdit")
        widgets = [
            (self.dialog_facebook_url_text_label, self.dialog_facebook_url_edit),
            (self.dialog_x_url_text_label, self.dialog_x_url_edit),
            (self.dialog_instagram_url_text_label, self.dialog_instagram_url_edit),
            (self.dialog_linkedin_url_text_label, self.dialog_linkedin_url_edit),
            (self.dialog_github_url_text_label, self.dialog_github_url_edit),
            (self.dialog_website_text_label, self.dialog_website_edit),
        ]
        for label, edit in widgets:
            main_layout.addRow(label, edit)
        return main_layout

    def set_ui_text(self) -> None:
        ui_text = LanguageProvider.get_dialog_text(self.objectName())
        widgets = self.findChildren((QLabel, QLineEdit))
        try:
            for widget in widgets:
                if isinstance(widget, QLabel):
                    if widget.objectName() in ui_text:
                        widget.setText(ui_text[widget.objectName()])
                elif isinstance(widget, QLineEdit):
                    if widget.objectName() in ui_text:
                        widget.setPlaceholderText(ui_text[widget.objectName()])
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def return_social_network_data(self) -> Optional[list]:
        error_text = LanguageProvider.get_error_text(self.objectName())
        inputs = self.findChildren(QLineEdit)
        social_network_data = []
        try:
            for widget in inputs:
                text = widget.text().strip()
                site = widget.objectName().replace("dialog", "").replace("UrlEdit", "")
                if text:
                    if site.lower() == "website" and not ContactValidator.validate_url(text, site):
                        DialogsProvider.show_error_dialog(error_text["websiteValidatorError"], self)
                        self.set_tab_index()
                        widget.setFocus()
                        return None
                    if not ContactValidator.validate_url(text, site):
                        message = error_text["urlValidatorError"].replace("{site}", site)
                        DialogsProvider.show_error_dialog(message, self)
                        self.set_tab_index()
                        widget.setFocus()
                        return None
                social_network_data.append(text)
            return social_network_data
        except Exception as e:
            ErrorHandler.exception_handler(e, self)
            return None

    def set_contact_data(self, data: dict) -> None:
        self.dialog_facebook_url_edit.setText(data["facebook_url"])
        self.dialog_x_url_edit.setText(data["x_url"])
        self.dialog_instagram_url_edit.setText(data["instagram_url"])
        self.dialog_linkedin_url_edit.setText(data["linkedin_url"])
        self.dialog_github_url_edit.setText(data["github_url"])
        self.dialog_website_edit.setText(data["website_url"])

    def set_tab_index(self) -> None:
        self.main_tab.setCurrentIndex(1)
        self.non_mandatory_tab.setCurrentIndex(1)