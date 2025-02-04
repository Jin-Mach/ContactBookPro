from PyQt6.QtWidgets import QDialog, QTabWidget, QLayout, QVBoxLayout

from src.contacts.ui.dialogs.dialog_widgets.mandatory_widget import MandatoryWidget
from src.contacts.ui.dialogs.dialog_widgets.non_mandatory_widget import NonMandatoryWidget


class ContactDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("contactDialog")
        self.setWindowTitle("dialog")
        self.setMinimumSize(500, 500)
        self.mandatory_widget = MandatoryWidget(self)
        self.non_mandatory_widget = NonMandatoryWidget(self)
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        dialog_tab_widget = QTabWidget()
        dialog_tab_widget.setObjectName("dialogTabWidget")
        self.madatory_tab_text = "mandatory"
        self.non_mandatory_tab_text = "non mandatory"
        dialog_tab_widget.addTab(self.mandatory_widget, self.madatory_tab_text)
        dialog_tab_widget.addTab(self.non_mandatory_widget, self.non_mandatory_tab_text)
        main_layout.addWidget(dialog_tab_widget)
        return main_layout