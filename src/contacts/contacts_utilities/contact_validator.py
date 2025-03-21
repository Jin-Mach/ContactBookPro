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
