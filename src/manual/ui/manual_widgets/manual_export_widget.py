from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout, QTabWidget, QTextEdit

from src.manual.utilities.set_tab_texts import apply_tab_texts


class ManualExportWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("manualExportWidget")
        self.setLayout(self.create_gui())
        tab_widgets = [self.csv_export_text_edit, self.excel_export_text_edit, self.vcard_export_text_edit]
        apply_tab_texts(self.objectName(), self.manual_export_tab_widget, tab_widgets, self)

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.manual_export_tab_widget = QTabWidget()
        self.csv_export_text_edit = QTextEdit()
        self.csv_export_text_edit.setObjectName("csvExportTextEdit")
        self.csv_export_text_edit.setReadOnly(True)
        self.csv_export_text_edit.setText("csv")
        self.excel_export_text_edit = QTextEdit()
        self.excel_export_text_edit.setObjectName("excelExportTextEdit")
        self.excel_export_text_edit.setReadOnly(True)
        self.excel_export_text_edit.setText("excel")
        self.vcard_export_text_edit = QTextEdit()
        self.vcard_export_text_edit.setObjectName("vcardExportTextEdit")
        self.vcard_export_text_edit.setReadOnly(True)
        self.vcard_export_text_edit.setText("vcard")
        self.manual_export_tab_widget.addTab(self.csv_export_text_edit, "")
        self.manual_export_tab_widget.addTab(self.excel_export_text_edit, "")
        self.manual_export_tab_widget.addTab(self.vcard_export_text_edit, "")
        main_layout.addWidget(self.manual_export_tab_widget)
        return main_layout

    def set_current_tab(self, index: int) -> None:
        self.manual_export_tab_widget.setCurrentIndex(index)