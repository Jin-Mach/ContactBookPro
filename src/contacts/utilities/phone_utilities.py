import phonenumbers

def format_phone_number(phone_number: str) -> str:
    if not phone_number:
        return ""
    parsed_number = phonenumbers.parse(phone_number, None)
    return str(phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL))