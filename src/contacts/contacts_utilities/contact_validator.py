import re
from typing import Optional

from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QLineEdit
from email_validator import validate_email, EmailNotValidError
import phonenumbers
from urllib.parse import urlparse
import tldextract
import validators


class ContactValidator:

    @staticmethod
    def validate_email(email: str) -> bool:
        try:
            validate_email(email, check_deliverability=False)
            return True
        except EmailNotValidError:
            return False

    @staticmethod
    def validate_phone_number(phone_number: str) -> bool:
        try:
            parsed_number = phonenumbers.parse(phone_number, None)
            return phonenumbers.is_valid_number(parsed_number)
        except phonenumbers.NumberParseException:
            return False

    @staticmethod
    def validate_url(url: str, site: str) -> bool:
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            url = "https://" + url
            parsed_url = urlparse(url)
        if site.lower() == "website":
            return validators.url(url)
        domain = tldextract.extract(parsed_url.netloc).domain
        if domain == "twitter":
            domain = "x"
        return domain == site.lower() and validators.url(url)

    @staticmethod
    def validate_work_address(address: QLineEdit, post_code: QLineEdit, city: QLineEdit, country: QLineEdit) -> bool:
        if (address.text().strip() and not post_code.text().strip()) or (not address.text().strip() and post_code.text().strip()):
            return False
        if (city.text().strip() and not country.text().strip()) or (not city.text().strip() and country.text().strip()):
            return False
        return True

    @staticmethod
    def contact_input_validator(email_edit: QLineEdit = None, phone_edit: QLineEdit = None, url_edit: list[QLineEdit] = None) -> None:
        email_regex = QRegularExpression(r"^[A-Za-z0-9@._+-]*$")
        phone_regex = QRegularExpression("^\\+[0-9]{1,14}$")
        url_regex = QRegularExpression(r"^[A-Za-z0-9:/?&=._%#\-]*$")
        email_validator = QRegularExpressionValidator(email_regex)
        phone_validator = QRegularExpressionValidator(phone_regex)
        url_validator = QRegularExpressionValidator(url_regex)
        if email_edit:
            email_edit.setValidator(email_validator)
        if phone_edit:
            phone_edit.setValidator(phone_validator)
        if url_edit:
            for edit in url_edit:
                edit.setValidator(url_validator)

    @staticmethod
    def search_input_validator(email_edit: QLineEdit = None, phone_edit: QLineEdit = None, url_edit: list[QLineEdit] = None,
                               birthday_edit: QLineEdit = None) -> None:
        email_regex = QRegularExpression(r"^[A-Za-z0-9@._+-]*$")
        phone_regex = QRegularExpression("^[+]?[0-9]{1,14}$")
        url_regex = QRegularExpression(r"^[A-Za-z0-9:/?&=._%#\-]*$")
        birthday_regex = QRegularExpression(r"^(?!\.)(\d+(\.\d+)*)?(?<!\.)$")
        email_validator = QRegularExpressionValidator(email_regex)
        phone_validator = QRegularExpressionValidator(phone_regex)
        url_validator = QRegularExpressionValidator(url_regex)
        birthday_validator = QRegularExpressionValidator(birthday_regex)
        if email_edit:
            email_edit.setValidator(email_validator)
        if phone_edit:
            phone_edit.setValidator(phone_validator)
        if url_edit:
            for edit in url_edit:
                edit.setValidator(url_validator)
        if birthday_edit:
            birthday_edit.setValidator(birthday_validator)

    @staticmethod
    def filter_name_input_validator(filter_name_edit: QLineEdit) -> None:
        filter_name_regex = QRegularExpression(r'^[\p{L}\d _-]+$')
        filter_name_validator = QRegularExpressionValidator(filter_name_regex)
        filter_name_edit.setValidator(filter_name_validator)

    @staticmethod
    def filter_invalid_characters(search_input: QLineEdit) -> Optional[str]:
        regex_pattern = None
        filtered_text = ""
        validator = search_input.validator()
        if validator:
            regex_exp_validator = validator.regularExpression()
            regex_pattern = regex_exp_validator.pattern()
        if regex_pattern:
            regex = re.compile(regex_pattern)
            for char in search_input.text().strip():
                if regex.match(char):
                    filtered_text += char
        return filtered_text