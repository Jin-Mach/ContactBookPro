from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout, QTabWidget, QTextEdit

from src.manual.utilities.set_tab_texts import apply_tab_texts


class ManualCheckWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("manualCheckWidget")
        self.setLayout(self.create_gui())
        tab_widgets = [self.check_birthday_text_edit, self.check_duplicity_text_edit, self.check_missing_coords_text_edit]
        apply_tab_texts(self.objectName(), self.manual_check_tab_widget, tab_widgets, self)

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.manual_check_tab_widget = QTabWidget()
        self.check_birthday_text_edit = QTextEdit()
        self.check_birthday_text_edit.setObjectName("checkBirthdayTextEdit")
        self.check_birthday_text_edit.setReadOnly(True)
        self.check_birthday_text_edit.setText("birthday")
        self.check_duplicity_text_edit = QTextEdit()
        self.check_duplicity_text_edit.setObjectName("checkDuplicityTextEdit")
        self.check_duplicity_text_edit.setReadOnly(True)
        self.check_duplicity_text_edit.setText("duplicity")
        self.check_missing_coords_text_edit = QTextEdit()
        self.check_missing_coords_text_edit.setObjectName("checkMissingCoordsTextEdit")
        self.check_missing_coords_text_edit.setReadOnly(True)
        self.check_missing_coords_text_edit.setText("coords")
        self.manual_check_tab_widget.addTab(self.check_birthday_text_edit, "")
        self.manual_check_tab_widget.addTab(self.check_duplicity_text_edit, "")
        self.manual_check_tab_widget.addTab(self.check_missing_coords_text_edit, "")
        main_layout.addWidget(self.manual_check_tab_widget)
        return main_layout

    def set_current_tab(self, index: int) -> None:
        self.manual_check_tab_widget.setCurrentIndex(index)