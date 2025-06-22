import qrcode
from PIL.Image import Image
from PyQt6.QtWidgets import QMainWindow

from src.utilities.error_handler import ErrorHandler


def create_qr_code(vcard_data: str, main_window: QMainWindow) -> Image | None:
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=4,
            border=2
        )
        qr.add_data(vcard_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#1e3a8a", back_color="#eaeaea")
        return img
    except Exception as e:
        ErrorHandler.exception_handler(e, main_window)
        return None