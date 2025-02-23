from PyQt6.QtWidgets import QDialog, QTabWidget, QLayout, QVBoxLayout

from src.contacts.ui.dialogs.dialog_widgets.mandatory_widget import MandatoryWidget
from src.contacts.ui.dialogs.dialog_widgets.non_mandatory_widget import NonMandatoryWidget
from src.utilities.error_handler import ErrorHandler
from src.utilities.language_provider import LanguageProvider


class ContactDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("contactDialog")
        self.setMinimumSize(650, 450)
        self.mandatory_widget = MandatoryWidget(self)
        self.non_mandatory_widget = NonMandatoryWidget(self)
        self.setLayout(self.create_gui())
        self.set_ui_text()

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.dialog_tab_widget = QTabWidget()
        self.dialog_tab_widget.setObjectName("dialogTabWidget")
        self.dialog_tab_widget.addTab(self.mandatory_widget, "")
        self.dialog_tab_widget.addTab(self.non_mandatory_widget, "")
        main_layout.addWidget(self.dialog_tab_widget)
        return main_layout

    def set_ui_text(self) -> None:
        ui_text = LanguageProvider.get_ui_text(self.objectName())
        tab_text = ["mandatory", "nonMandatory"]
        try:
            if "dialogTitle" in ui_text:
                self.setWindowTitle(ui_text["dialogTitle"])
            for index, text in enumerate(tab_text):
                if text in ui_text:
                    self.dialog_tab_widget.setTabText(index, ui_text[text])
        except Exception as e:
            ErrorHandler.exception_handler(e, self)