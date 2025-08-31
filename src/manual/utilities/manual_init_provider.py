from PyQt6.QtWidgets import QTextEdit, QWidget, QTabWidget

from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class ManualInitProvider:

    @staticmethod
    def apply_tab_texts(widget_object_name: str, tab_widget: QTabWidget, tab_widgets: list[QTextEdit],
                        parent: QWidget) -> None:
        try:
            ui_text = LanguageProvider.get_json_text("ui_text.json", widget_object_name)
            tab_texts = ui_text.get("tabTexts", {})
            for index, widget in enumerate(tab_widgets):
                if widget.objectName() in tab_texts:
                    tab_widget.setTabText(index, tab_texts.get(widget.objectName(), ""))
        except Exception as e:
            ErrorHandler.exception_handler(e, parent)

    @staticmethod
    def initialize_text_edits(text_edit_list: list[QTextEdit], parent: QWidget) -> None:
        try:
            edit_names = []
            for text_edit in text_edit_list:
                edit_names.append(text_edit.objectName())
            text = LanguageProvider.get_document_text("manual", edit_names)
            for text_edit in text_edit_list:
                text_edit.setPlainText(text.get(text_edit.objectName(), ""))
                text_edit.setStyleSheet("font: Arial; font-size: 15pt;")
                text_edit.setReadOnly(True)
        except Exception as e:
            ErrorHandler.exception_handler(e, parent)