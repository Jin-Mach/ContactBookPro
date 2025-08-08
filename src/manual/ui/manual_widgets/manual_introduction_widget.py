from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout, QTabWidget, QTextEdit

from src.manual.utilities.set_tab_texts import apply_tab_texts


class ManualIntroductionWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("manualIntroductionWidget")
        self.setLayout(self.create_gui())
        tab_widgets = [self.about_application_text_edit, self.usage_manual_text_edit]
        apply_tab_texts(self.objectName(), self.manual_introduction_tab_widget, tab_widgets, self)

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.manual_introduction_tab_widget = QTabWidget()
        self.about_application_text_edit = QTextEdit()
        self.about_application_text_edit.setObjectName("aboutApplicationTextEdit")
        self.about_application_text_edit.setReadOnly(True)
        self.about_application_text_edit.setText("about")
        self.usage_manual_text_edit = QTextEdit()
        self.usage_manual_text_edit.setObjectName("usageApplicationTextEdit")
        self.usage_manual_text_edit.setReadOnly(True)
        self.usage_manual_text_edit.setText("usage")
        self.manual_introduction_tab_widget.addTab(self.about_application_text_edit, "")
        self.manual_introduction_tab_widget.addTab(self.usage_manual_text_edit, "")
        main_layout.addWidget(self.manual_introduction_tab_widget)
        return main_layout

    def set_current_tab(self, index: int) -> None:
        self.manual_introduction_tab_widget.setCurrentIndex(index)