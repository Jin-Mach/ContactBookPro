from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QPushButton, QHBoxLayout

from src.contacts.ui.preview_widgets.pdf_view import PdfView
from src.utilities.error_handler import ErrorHandler
from src.utilities.icon_provider import IconProvider
from src.utilities.language_provider import LanguageProvider


# noinspection PyUnresolvedReferences
class PdfPreviewDialog(QDialog):
    def __init__(self, pdf_path: str, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("pdfPreviewDialog")
        self.setMinimumSize(600, 700)
        self.pdf_path = pdf_path
        self.parent = parent
        self.pdf_view = PdfView(self.pdf_path, self)
        if not self.pdf_view.document_sate:
            raise ValueError()
        self.setLayout(self.create_gui())
        self.buttons = self.findChildren(QPushButton)
        self.set_ui_text()
        self.set_tooltips_text()
        self.create_connection()
        IconProvider.set_buttons_icon(self.objectName(), self.buttons, QSize(30, 30), self.parent)

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        toolbar_layout = QHBoxLayout()
        self.print_button = QPushButton()
        self.print_button.setObjectName("pdfPrintButton")
        self.save_as_button = QPushButton()
        self.save_as_button.setObjectName("pdfSaveAsButton")
        self.fit_page_button = QPushButton()
        self.fit_page_button.setObjectName("pdfFitPageButton")
        self.zoom_in_button = QPushButton()
        self.zoom_in_button.setObjectName("pdfZoomInButton")
        self.zoom_out_button = QPushButton()
        self.zoom_out_button.setObjectName("pdfZoomOutButton")
        self.pdf_view_widget = self.pdf_view
        button_layout = QHBoxLayout()
        self.close_dialog_button = QPushButton()
        self.close_dialog_button.setObjectName("closeDialogButton")
        toolbar_layout.addWidget(self.print_button)
        toolbar_layout.addWidget(self.save_as_button)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.fit_page_button)
        toolbar_layout.addWidget(self.zoom_in_button)
        toolbar_layout.addWidget(self.zoom_out_button)
        button_layout.addStretch()
        button_layout.addWidget(self.close_dialog_button)
        main_layout.addLayout(toolbar_layout)
        main_layout.addWidget(self.pdf_view_widget)
        main_layout.addLayout(button_layout)
        return main_layout

    def set_ui_text(self) -> None:
        try:
            ui_text = LanguageProvider.get_preview_dialog_text(self.objectName())
            if "pdfDialogTitle" in ui_text:
                self.setWindowTitle(ui_text.get("pdfDialogTitle", ""))
            for button in self.buttons:
                if button.objectName() in ui_text:
                    button.setText(ui_text.get(button.objectName(), ""))
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def set_tooltips_text(self) -> None:
        try:
            tooltips_text = LanguageProvider.get_tooltips_text(self.objectName())
            for button in self.buttons:
                if button.objectName() in tooltips_text:
                    button.setToolTip(tooltips_text.get(button.objectName(), ""))
                    button.setToolTipDuration(5000)
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def create_connection(self) -> None:
        connections = [
            #(self.print_button, self.pdf_view.test),
            #(self.save_as_button, print("save")),
            (self.zoom_in_button, self.pdf_view_widget.zoom_in),
            (self.zoom_out_button, self.pdf_view_widget.zoom_out),
            (self.fit_page_button, self.pdf_view_widget.reset_zoom),
            (self.close_dialog_button, self.close)
        ]
        try:
            for button, method in connections:
                button.clicked.connect(method)
        except Exception as e:
            ErrorHandler.exception_handler(e, self.parent)

    def closeEvent(self, event) -> None:
        if self.pdf_view.document():
            self.pdf_view.document().close()
            self.pdf_view.document().deleteLater()
        super().closeEvent(event)