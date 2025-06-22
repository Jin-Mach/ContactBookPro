import vobject
from PyQt6.QtWidgets import QMainWindow

from src.utilities.error_handler import ErrorHandler


def create_vcard(row_data: dict, main_window: QMainWindow) -> str | None:
    try:
        row_data = row_data
        vcard = vobject.vCard()
        full_name = f"{row_data.get("first_name", "")} {row_data.get("second_name", "")}".strip()
        vcard.add("fn").value = full_name
        personal_name = vcard.add("n")
        personal_name.value = vobject.vcard.Name(
            given = row_data.get("first_name", ""),
            family = row_data.get("second_name", "")
        )
        personal_email = vcard.add("email")
        personal_email.value = row_data.get("personal_email", "")
        personal_email.params["TYPE"] = ["HOME"]
        personal_phone_number = vcard.add("tel")
        personal_phone_number.value = row_data.get("personal_phone_number", "")
        personal_phone_number.params["TYPE"] = ["MAIN"]
        contact_street = row_data.get("personal_house_number", "")
        if row_data.get("personal_street"):
            contact_street = f"{row_data.get('personal_street', '')} {row_data.get('personal_house_number', '')}"
        personal_address = vcard.add("adr")
        personal_address.value = vobject.vcard.Address(
            street = contact_street,
            city = row_data.get("personal_city", ""),
            code = row_data.get("personal_post_code", ""),
            country = row_data.get("personal_country", ""),
            box = "",
            extended = "",
            region = ""
        )
        personal_address.params["TYPE"] = ["HOME"]
        return vcard.serialize()
    except Exception as e:
        ErrorHandler.exception_handler(e, main_window)
        return None