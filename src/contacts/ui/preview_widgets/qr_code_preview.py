import qrcode.image.pil
from PIL.ImageQt import ImageQt
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QLabel

from src.utilities.error_handler import ErrorHandler
from src.utilities.icon_provider import IconProvider
from src.utilities.language_provider import LanguageProvider


class QrCodePreviewDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("qrCodePreviewDialog")
        self.setFixedSize(400, 500)
        self.setLayout(self.create_gui())
        self.set_ui_text()
        IconProvider.set_window_icon(self, self.objectName())

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.contact_name_label = QLabel()
        self.contact_name_label.setStyleSheet("font-family: Arial; font-size: 20pt;")
        self.contact_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qr_code_label = QLabel()
        self.qr_code_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label_text = QLabel()
        self.info_label_text.setObjectName("infoLabelText")
        self.info_label_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.contact_name_label)
        main_layout.addStretch()
        main_layout.addWidget(self.qr_code_label)
        main_layout.addStretch()
        main_layout.addWidget(self.info_label_text)
        return main_layout

    def set_ui_text(self) -> None:
        try:
            ui_text = LanguageProvider.get_preview_dialog_text(self.objectName())
            widgets = self.findChildren(QLabel)
            if ui_text:
                if "qrDialogTitle" in ui_text:
                    self.setWindowTitle(ui_text.get("qrDialogTitle", ""))
                for widget in widgets:
                    if widget.objectName() in ui_text:
                        widget.setText(ui_text.get(widget.objectName(), ""))
        except Exception as e:
            ErrorHandler.exception_handler(e, self)

    def set_labels_texts(self, contact_name: str, qr_code: qrcode.image.pil.PilImage) -> None:
        try:
            self.contact_name_label.setText(contact_name)
            pil_image = qr_code.get_image()
            qr_image = ImageQt(pil_image)
            qr_pixmap = QPixmap.fromImage(qr_image)
            self.qr_code_label.setPixmap(qr_pixmap)
        except Exception as e:
            ErrorHandler.exception_handler(e, self)