from email_validator import validate_email, EmailNotValidError
import phonenumbers


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
        if not phone_number.startswith("+"):
            phone_number = "+" + phone_number.lstrip("+")
        try:
            parsed_number = phonenumbers.parse(phone_number, None)
            return phonenumbers.is_valid_number(parsed_number)
        except phonenumbers.NumberParseException:
            return False