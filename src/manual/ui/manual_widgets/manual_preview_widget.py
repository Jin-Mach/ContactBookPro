from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout, QTabWidget, QTextEdit

from src.manual.utilities.set_tab_texts import apply_tab_texts


class ManualPreviewWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("manualPreviewWidget")
        self.setLayout(self.create_gui())
        tab_widgets = [self.pdf_text_edit, self.qr_code_text_edit]
        apply_tab_texts(self.objectName(), self.manual_preview_tab_widget, tab_widgets, self)

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.manual_preview_tab_widget = QTabWidget()
        self.pdf_text_edit = QTextEdit()
        self.pdf_text_edit.setObjectName("pdfPreviewTextEdit")
        self.pdf_text_edit.setReadOnly(True)
        self.pdf_text_edit.setText("pdf")
        self.qr_code_text_edit = QTextEdit()
        self.qr_code_text_edit.setObjectName("qrCodePreviewTextEdit")
        self.qr_code_text_edit.setReadOnly(True)
        self.qr_code_text_edit.setText("qr code")
        self.manual_preview_tab_widget.addTab(self.pdf_text_edit, "")
        self.manual_preview_tab_widget.addTab(self.qr_code_text_edit, "")
        main_layout.addWidget(self.manual_preview_tab_widget)
        return main_layout

    def set_current_tab(self, index: int) -> None:
        self.manual_preview_tab_widget.setCurrentIndex(index)