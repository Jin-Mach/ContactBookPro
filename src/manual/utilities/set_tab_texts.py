from PyQt6.QtWidgets import QTextEdit, QWidget, QTabWidget

from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


def apply_tab_texts(widget_object_name: str, tab_widget: QTabWidget, tab_widgets: list[QTextEdit], parent: QWidget) -> None:
    try:
        ui_text = LanguageProvider.get_ui_text(widget_object_name)
        tab_texts = ui_text.get("tabTexts", {})
        for index, widget in enumerate(tab_widgets):
            if widget.objectName() in tab_texts:
                tab_widget.setTabText(index, tab_texts.get(widget.objectName(), ""))
    except Exception as e:
        ErrorHandler.exception_handler(e, parent)
