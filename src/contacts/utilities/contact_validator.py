import re
import phonenumbers
import tldextract
import validators

from urllib.parse import urlparse
from email_validator import validate_email, EmailNotValidError

from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QLineEdit


# noinspection PyUnresolvedReferences
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
        domain = tldextract.extract(parsed_url.netloc).domain
        ext = tldextract.extract(parsed_url.netloc)
        if not ext.suffix:
            return False
        if site.lower() == "website":
            return validators.url(url)
        if domain == "twitter":
            domain = "x"
        return domain == site.lower() and bool(ext.suffix) and validators.url(url)

    @staticmethod
    def validate_work_address(house_number: QLineEdit, city: QLineEdit, post_code: QLineEdit, country: QLineEdit) -> bool:
        all_empty = (not house_number.text().strip() and not city.text().strip() and not post_code.text().strip()
                     and not country.text().strip())
        all_filled = (house_number.text().strip() and city.text().strip() and post_code.text().strip()
                     and country.text().strip())
        return all_empty or all_filled


    @staticmethod
    def contact_input_validator(name_city_edits: list[QLineEdit] = None, house_number_edit: QLineEdit = None,
                                post_code_edit: QLineEdit = None, email_edit: QLineEdit = None,
                                phone_edit: QLineEdit = None,company_edit: QLineEdit = None, url_edit: list[QLineEdit] = None,
                                title_edit: QLineEdit = None) -> None:
        name_city_regex = QRegularExpression(r"^[\p{L} \-']*$")
        house_number_regex = QRegularExpression(r"^[0-9A-Za-z/\-]*$")
        post_code_regex = QRegularExpression(r"[A-Za-z0-9 \-]*")
        email_regex = QRegularExpression(r"^[A-Za-z0-9@._+-]*$")
        phone_regex = QRegularExpression("^\\+[0-9]{1,14}$")
        company_regex = QRegularExpression(r"^[\p{L}0-9 &.,()'\"-]*$")
        url_regex = QRegularExpression(r"^[A-Za-z0-9:/?&=._%#\-]*$")
        title_regex = QRegularExpression(r"^[A-Za-zÀ-ž .,'\-]{1,100}$")
        name_city_validator = QRegularExpressionValidator(name_city_regex)
        house_number_validator = QRegularExpressionValidator(house_number_regex)
        post_code_validator = QRegularExpressionValidator(post_code_regex)
        email_validator = QRegularExpressionValidator(email_regex)
        phone_validator = QRegularExpressionValidator(phone_regex)
        company_validator = QRegularExpressionValidator(company_regex)
        url_validator = QRegularExpressionValidator(url_regex)
        title_validator = QRegularExpressionValidator(title_regex)
        if name_city_edits:
            for line_edit in name_city_edits:
                line_edit.setValidator(name_city_validator)
        if house_number_edit:
            house_number_edit.setValidator(house_number_validator)
        if post_code_edit:
            post_code_edit.setValidator(post_code_validator)
        if email_edit:
            email_edit.setValidator(email_validator)
        if phone_edit:
            phone_edit.setValidator(phone_validator)
        if company_edit:
            company_edit.setValidator(company_validator)
        if url_edit:
            for edit in url_edit:
                edit.setValidator(url_validator)
        if title_edit:
            title_edit.setValidator(title_validator)

    @staticmethod
    def search_input_validator(name_city_edits: list[QLineEdit] = None, house_number_edit: QLineEdit = None,
                               post_code_edit: QLineEdit = None, email_edit: QLineEdit = None,
                               phone_edit: QLineEdit = None, company_edit: QLineEdit = None,
                               url_edit: list[QLineEdit] = None, title_edit: QLineEdit = None,
                               birthday_edit: QLineEdit = None) -> None:
        name_city_regex = QRegularExpression(r"[\p{L} \-']*")
        house_number_regex = QRegularExpression(r"[0-9A-Za-z/\-]*")
        post_code_regex = QRegularExpression(r"[A-Za-z0-9 \-]*")
        email_regex = QRegularExpression(r"[A-Za-z0-9@._+-]*")
        phone_regex = QRegularExpression(r"[+]?[0-9]*")
        company_regex = QRegularExpression(r"[\p{L}0-9 &.,()'\"-]*")
        url_regex = QRegularExpression(r"[A-Za-z0-9:/?&=._%#\-]*")
        title_regex = QRegularExpression(r"[A-Za-zÀ-ž .,'\-]*")
        birthday_regex = QRegularExpression(r"\d{0,2}(\.\d{0,2}(\.\d{0,4})?)?")
        name_city_validator = QRegularExpressionValidator(name_city_regex)
        house_number_validator = QRegularExpressionValidator(house_number_regex)
        post_code_validator = QRegularExpressionValidator(post_code_regex)
        email_validator = QRegularExpressionValidator(email_regex)
        phone_validator = QRegularExpressionValidator(phone_regex)
        company_validator = QRegularExpressionValidator(company_regex)
        url_validator = QRegularExpressionValidator(url_regex)
        title_validator = QRegularExpressionValidator(title_regex)
        birthday_validator = QRegularExpressionValidator(birthday_regex)
        if name_city_edits:
            for line_edit in name_city_edits:
                line_edit.setValidator(name_city_validator)
        if house_number_edit:
            house_number_edit.setValidator(house_number_validator)
        if post_code_edit:
            post_code_edit.setValidator(post_code_validator)
        if email_edit:
            email_edit.setValidator(email_validator)
        if phone_edit:
            phone_edit.setValidator(phone_validator)
        if company_edit:
            company_edit.setValidator(company_validator)
        if url_edit:
            for edit in url_edit:
                edit.setValidator(url_validator)
        if title_edit:
            title_edit.setValidator(title_validator)
        if birthday_edit:
            birthday_edit.setValidator(birthday_validator)

    @staticmethod
    def filter_name_input_validator(filter_name_edit: QLineEdit) -> None:
        filter_name_regex = QRegularExpression(r'^[\p{L}\d _-]+$')
        filter_name_validator = QRegularExpressionValidator(filter_name_regex)
        filter_name_edit.setValidator(filter_name_validator)

    @staticmethod
    def filter_invalid_characters(search_input: QLineEdit) -> str | None:
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